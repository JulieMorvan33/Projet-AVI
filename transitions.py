import geometry as g
import numpy as np
from constantParameters import *

EPSILON = 5


def compute_transition_fly_by(seg_actif, seg_next):
	"""Compute track_change, turn radius, seg_actif, seg_next, b_in, b_out, b_center
	associated to the index i transition """

	#Recuperation des points A (debut) et B (fin) du premier segment
	a = seg_actif.start
	b = seg_actif.end

	#calcul du track change entre les deux segments
	track_change = np.arccos((seg_actif.scal(seg_next)) / (seg_actif.norm() * seg_next.norm())) * RAD2DEG  # en degrés
	#print("track_change=", track_change) #en degré

	#calcul bank_angle, turn_radius et lead_distance

	if ALTITUDE>195:
		max_angle = (16 - 25) / (300 - 195) * (ALTITUDE - 195) + 25
		bank_angle = max(5, min(0.5 * track_change, max_angle)) #en DEG
		turn_radius = GS ** 2 / (G * np.tan(bank_angle / RAD2DEG)) / NM2M  # NM
		lead_distance = turn_radius * np.tan(0.5 * track_change / RAD2DEG)  # NM
		if lead_distance > 20:  # NM
			lead_distance = 20  # NM
			turn_radius = lead_distance / np.tan(0.5 * track_change / RAD2DEG)
			bank_angle = max(5, min(np.arctan(GS ** 2) / (G * turn_radius), max_angle))
		#print("lead_distance", lead_distance)
	else :
		max_angle = 25 #DEG
		bank_angle = max(5, min(0.5*track_change,max_angle)) #DEG
		turn_radius = GS**2 / (G*np.tan(bank_angle / RAD2DEG)) / NM2M # NM
		lead_distance = turn_radius * np.tan(0.5 * track_change / RAD2DEG)

	#calcul de b_in et b_out : points de debut et fin de la transition en arc de cercle
	if track_change < EPSILON: #mettre zero
		b_in = b
		b_out = b
		b_center = b #rajouter lead et radius = 0

	else:
		norme_act = seg_actif.norm()
		active_track = get_track(seg_actif)  # en RAD
		next_track = get_track(seg_next)
		b_in = calcul_point_de_transition(a, norme_act, lead_distance, active_track)
		b_out = calcul_point_de_transition(b, lead_distance, 0, next_track)

		#calcul de l'angle a_b_bcenter et du point b_center (centre de l'arc de transition)

		d = (turn_radius ** 2 + lead_distance ** 2) ** 0.5
		if seg_actif.det(seg_next) > 0:
			a_b_bc_angle = ((180 + track_change) / 2) / RAD2DEG  # en rad
			b_center = g.Point(b.x - d * np.sin((a_b_bc_angle-active_track)),
						 b.y + d * np.cos((a_b_bc_angle-active_track)))
			bank_angle = - bank_angle

		else:
			a_b_bc_angle = ((180 - track_change) / 2) / RAD2DEG
			b_center = g.Point(b.x + d * np.sin((a_b_bc_angle-active_track)),
						 b.y - d * np.cos((a_b_bc_angle-active_track)))

	return(track_change, turn_radius, b_in, b_out, b_center, lead_distance, bank_angle)


def compute_transition_fly_over(seg_actif, seg_next):
	# Recuperation des points A (debut) et B (fin) du premier segment
	a = seg_actif.start
	b = seg_actif.end

	# calcul du track change entre les deux segments
	track_change = np.arccos((seg_actif.scal(seg_next)) / (seg_actif.norm() * seg_next.norm())) * RAD2DEG +30 # en degrés

	if ALTITUDE>195:
		max_angle = (16 - 25) / (300 - 195) * (ALTITUDE - 195) + 25
		bank_angle = max(5, min(0.5 * track_change, max_angle)) #en DEG
		turn_radius = GS ** 2 / (G * np.tan(bank_angle / RAD2DEG)) / NM2M  # NM
		lead_distance = turn_radius * np.tan(0.5 * track_change / RAD2DEG)  # NM
		if lead_distance > 20:  # NM
			lead_distance = 20  # NM
			turn_radius = lead_distance / np.tan(0.5 * track_change / RAD2DEG)
			bank_angle = max(5, min(np.arctan(GS ** 2) / (G * turn_radius), max_angle))
		#print("lead_distance", lead_distance)
	else :
		max_angle = 25 #DEG
		bank_angle = max(5, min(0.5*track_change,max_angle)) #DEG
		turn_radius = GS**2 / (G*np.tan(bank_angle / RAD2DEG)) / NM2M # NM
		lead_distance = turn_radius * np.tan(0.5 * track_change / RAD2DEG)

	# if track_change < EPSILON:
	# 	b_in = b
	# 	b_out = b
	# 	b_center = b

	b_in = b
	active_track = get_track(seg_actif)
	im_1 = g.Point(b.x + lead_distance*np.sin(active_track),
				   b.y+lead_distance*np.cos(active_track))
	norme_act = seg_actif.norm()
	next_track = get_track(seg_next)
	if seg_actif.det(seg_next)>0:
		if abs(next_track)<np.pi-np.pi/6:
			next_track_im = next_track - np.pi/6
		else:
			next_track_im = next_track - np.pi/6 - np.sign(next_track)*2*np.pi
	else:
		if abs(next_track)<np.pi-np.pi/6:
			next_track_im = next_track + np.pi/6
		else:
			next_track_im = next_track + np.pi/6 - np.sign(next_track)*2*np.pi
	print(next_track_im*RAD2DEG, next_track*RAD2DEG)
	seg_next_im = g.Segment(im_1, g.Point(im_1.x + 10*lead_distance*np.sin(next_track_im),
										  im_1.y + 10*lead_distance*np.cos(next_track_im)))
	b_out = calcul_point_de_transition(im_1, lead_distance, 0, next_track_im)

	# calcul de l'angle a_b_bcenter et du point b_center (centre de l'arc de transition)

	d = (turn_radius ** 2 + lead_distance ** 2) ** 0.5
	if seg_actif.det(seg_next_im) > 0:
		a_b_bc_angle = ((180 + track_change) / 2) / RAD2DEG  # en rad
		b_center = g.Point(im_1.x - d * np.sin((a_b_bc_angle - active_track)),
						   im_1.y + d * np.cos((a_b_bc_angle - active_track)))
		bank_angle = - bank_angle

	else:
		a_b_bc_angle = ((180 - track_change) / 2) / RAD2DEG
		b_center = g.Point(im_1.x + d * np.sin((a_b_bc_angle - active_track)),
						   im_1.y - d * np.cos((a_b_bc_angle - active_track)))

	# active_track = get_track(seg_actif)
	# if seg_actif.det(seg_next) > 0:
	# 	b_center = g.Point(b.x - turn_radius*np.sin((np.pi/2-active_track)),
	# 					   b.y + turn_radius*np.cos((np.pi/2-active_track)))
	# 	next_track = get_track(seg_next)
	# 	b_out = g.Point(b_center.x + turn_radius*np.sin(next_track+np.pi/3),
	# 					b_center.y + turn_radius*np.cos(next_track+np.pi/3))
	# else:
	# 	b_center = g.Point(b.x + turn_radius * np.sin((np.pi / 2 - active_track)),
	# 					   b.y - turn_radius * np.cos((np.pi / 2 - active_track)))
	# 	next_track = get_track(seg_next)
	# 	b_out = g.Point(b_center.x + turn_radius * np.sin(next_track - np.pi / 3),
	# 					b_center.y + turn_radius * np.cos(next_track - np.pi / 3))

	return (track_change, turn_radius, b_in, b_out, b_center, lead_distance, bank_angle)

def get_track(segment_courant):
	"""La route est calculee en RAD, entre -pi et pi"""

	# construction segment vertical pour calculer la route.
	seg_calcul = g.Segment(segment_courant.start, g.Point(segment_courant.start.x,segment_courant.start.y + 100))
	track = np.arccos(seg_calcul.scal(segment_courant)/
					  ((seg_calcul.norm())*(segment_courant.norm())))

	#track positive pour un virage a droite
	if seg_calcul.det(segment_courant)>0:
		#print("track=", -track * (RAD2DEG))
		return -track #en RAD
	else :
		#print("track=", track * (RAD2DEG))
		return track #en RAD

def calcul_point_de_transition(origine, dist_segment, lead_dist,track):
	return g.Point(origine.x + (dist_segment - lead_dist) * np.sin(track),
				   origine.y + (dist_segment - lead_dist) * np.cos(track))

