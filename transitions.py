import geometry as g
import numpy as np
from constantParameters import *

EPSILON = 10e-5
#Transition parameters
intersect_angle = np.pi/6

def compute_transition_fly_by(seg_actif, seg_next, TAS):
	"""Compute track_change, turn radius, seg_actif, seg_next, b_in, b_out, b_center
	associated to the index i transition """

	#Recuperation des points A (debut) et B (fin) du premier segment
	a = seg_actif.start
	b = seg_actif.end

	#calcul du track change entre les deux segments
	track_change = np.arccos((seg_actif.scal(seg_next)) / (seg_actif.norm() * seg_next.norm())) * RAD2DEG  # en degrés
	print("track_change=", track_change) #en degré

	#si pas de virage :
	if track_change < EPSILON:
		return [g.Arc(b, b, b, 0, 0, 0, 0, 0)]

	#si virage :
	else :
		# calcul bank_angle, turn_radius et lead_distance
		if ALTITUDE>195:
			max_angle = (16 - 25) / (300 - 195) * (ALTITUDE - 195) + 25
			bank_angle = max(5, min(0.5 * track_change, max_angle)) #en DEG
			turn_radius = TAS ** 2 / (G * np.tan(bank_angle / RAD2DEG)) / NM2M  # NM
			lead_distance = turn_radius * np.tan(0.5 * track_change / RAD2DEG)  # NM
			if lead_distance > 20:  # NM
				lead_distance = 20  # NM
				turn_radius = lead_distance / np.tan(0.5 * track_change / RAD2DEG)
				bank_angle = max(5, min(np.arctan(TAS ** 2) / (G * turn_radius), max_angle))
			#print("lead_distance", lead_distance)
		else :
			max_angle = 25 #DEG
			bank_angle = max(5, min(0.5*track_change,max_angle)) #DEG
			turn_radius = TAS**2 / (G*np.tan(bank_angle / RAD2DEG)) / NM2M # NM
			lead_distance = turn_radius * np.tan(0.5 * track_change / RAD2DEG)

		#calcul de b_in et b_out : points de debut et fin de la transition en arc de cercle
		norme_act = seg_actif.norm()
		active_track = get_track(seg_actif)  # en RAD
		next_track = get_track(seg_next)
		b_in = calcul_point_de_transition(a, norme_act, lead_distance, active_track)
		b_out = calcul_point_de_transition(b, lead_distance, 0, next_track)

		#calcul de l'angle a_b_bcenter et du point b_center (centre de l'arc de transition)

		d = (turn_radius ** 2 + lead_distance ** 2) ** 0.5
		sens_virage = seg_actif.det(seg_next)
		if sens_virage > 0:
			a_b_bc_angle = ((180 + track_change) / 2) / RAD2DEG  # en rad
			b_center = g.Point(b.x - d * np.sin((a_b_bc_angle-active_track)),
						 b.y + d * np.cos((a_b_bc_angle-active_track)))
			bank_angle = - bank_angle

		else:
			a_b_bc_angle = ((180 - track_change) / 2) / RAD2DEG
			b_center = g.Point(b.x + d * np.sin((a_b_bc_angle-active_track)),
							   b.y - d * np.cos((a_b_bc_angle-active_track)))
	return [g.Arc(b_center, b_in, b_out, turn_radius, lead_distance, bank_angle, track_change, sens_virage)]


def compute_transition_fly_over(seg_actif, seg_next, TAS):
	# Recuperation des points A (debut) et B (fin) du premier segment
	a = seg_actif.start
	b = seg_actif.end

	# calcul du track change entre les deux segments
	track_change_initial = np.arccos((seg_actif.scal(seg_next)) / (seg_actif.norm() * seg_next.norm()))* RAD2DEG
	if track_change_initial < 60 :
		intersect_angle = track_change_initial/(3*RAD2DEG)# en degrés
	else:
		intersect_angle = np.pi/6
	track_change = track_change_initial + intersect_angle*RAD2DEG

	# si pas de virage :
	if track_change_initial < EPSILON:
		arc = g.Arc(b, b, b, 0, 0, 0, 0, 0)
		segment_jointif = g.Segment(b,b)
		return([arc, segment_jointif, arc])

	# si virage :
	else:
		if ALTITUDE>195:
			max_angle = (16 - 25) / (300 - 195) * (ALTITUDE - 195) + 25
			bank_angle = max(5, min(0.5 * track_change, max_angle)) #en DEG
			turn_radius = TAS ** 2 / (G * np.tan(bank_angle / RAD2DEG)) / NM2M  # NM
			lead_distance = turn_radius * np.tan(0.5 * track_change / RAD2DEG)  # NM
			if lead_distance > 20:  # NM
				lead_distance = 20  # NM
				turn_radius = lead_distance / np.tan(0.5 * track_change / RAD2DEG)
				bank_angle = max(5, min(np.arctan(TAS ** 2) / (G * turn_radius), max_angle))
			#print("lead_distance", lead_distance)
		else :
			max_angle = 25 #DEG
			bank_angle = max(5, min(0.5*track_change,max_angle)) #DEG
			turn_radius = TAS**2 / (G*np.tan(bank_angle / RAD2DEG)) / NM2M # NM
			lead_distance = turn_radius * np.tan(0.5 * track_change / RAD2DEG)

		im1_in = b
		active_track = get_track(seg_actif)
		im_1 = g.Point(b.x + lead_distance*np.sin(active_track),
					   b.y+lead_distance*np.cos(active_track))
		next_track = get_track(seg_next)
		if seg_actif.det(seg_next)>0:
			if abs(next_track)<np.pi-intersect_angle:
				next_track_im = next_track - intersect_angle
			else:
				next_track_im = next_track - intersect_angle - np.sign(next_track)*2*np.pi
		else:
			if abs(next_track)<np.pi-intersect_angle:
				next_track_im = next_track + intersect_angle
			else:
				next_track_im = next_track + intersect_angle - np.sign(next_track)*2*np.pi
		norme_next = seg_next.norm()
		seg_next_im = g.Segment(im_1, g.Point(im_1.x + 1.2*norme_next*np.sin(next_track_im),
											  im_1.y + 1.2*norme_next*np.cos(next_track_im)))
		im1_out = calcul_point_de_transition(im_1, lead_distance, 0, next_track_im)

		# calcul de l'angle a_b_bcenter et du point b_center (centre de l'arc de transition)

		d = (turn_radius ** 2 + lead_distance ** 2) ** 0.5
		sens_virage = seg_actif.det(seg_next_im)
		if sens_virage > 0:
			a_im1_im1c_angle = ((180 + track_change) / 2) / RAD2DEG  # en rad
			im1_center = g.Point(im_1.x - d * np.sin((a_im1_im1c_angle - active_track)),
							   im_1.y + d * np.cos((a_im1_im1c_angle - active_track)))
			bank_angle = - bank_angle

		else:
			a_im1_im1c_angle = ((180 - track_change) / 2) / RAD2DEG
			im1_center = g.Point(im_1.x + d * np.sin((a_im1_im1c_angle - active_track)),
							   im_1.y - d * np.cos((a_im1_im1c_angle - active_track)))

	arc1 = g.Arc(im1_center, im1_in, im1_out, turn_radius, lead_distance, bank_angle, track_change, sens_virage)

	#try:
	im_2 = seg_next_im.intersection(seg_next)
	im_1_im2 = g.Segment(im1_out,im_2)
	im_2_next = g.Segment(im_2, seg_next.end)
	l_arc2 = compute_transition_fly_by(im_1_im2, im_2_next, TAS)
	arc2 = l_arc2[0]
	segment_jointif = g.Segment(im1_out, arc2.start)
	return [arc1, segment_jointif, arc2]
	#except Exception:

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

