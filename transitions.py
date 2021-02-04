import geometry as g
import numpy as np
from constantParameters import *


# Pour comprendre plus efficacement ce module, il est vivement conseillé de le mettre en miroir
# avec la partie "Conception of the trajectory" du DFS

EPSILON = 10e-5


def compute_transition_fly_by(active_seg, next_seg, tas):
	"""Calcul une transition fly_by entre deux legs
	- entrées : les deux legs en question (active_seg et next_seg) et la True Air Speed (tas)
	- sortie: liste contenant un objet Arc représentant les paramètres de la transition"""

	# Recuperation des points A (debut) et B (fin) du premier segment. Cf le DFS pour voir le cas de calcul;
	# a et b correpondent au schémas du DFS
	a = active_seg.start
	b = active_seg.end

	# Calcul du track change entre les deux segments
	track_change = np.arccos((active_seg.scal(next_seg)) / (active_seg.norm() * next_seg.norm())) * RAD2DEG  # en
	# degrés, positif

	# Si pas de virage :
	if track_change < EPSILON:  # Epsilon pour comparaison à zéro
		return [g.Arc(b, b, b, 0, 0, 0, 0, 0)]  # Renvoi d'un arc nul dasn le cas d'une track change nulle

	# Si virage :
	else:
		# calcul bank_angle, turn_radius et lead_distance à partir de track_change, tas et ALTITUDE
		# Specs IENAC17 :
		if ALTITUDE > 195:
			max_angle = (16 - 25) / (300 - 195) * (ALTITUDE - 195) + 25  # en degrés
			bank_angle = max(5, min(0.5 * track_change, max_angle))  # en degrés
			turn_radius = tas ** 2 / (G * np.tan(bank_angle / RAD2DEG)) / NM2M  # NM
			lead_distance = turn_radius * np.tan(0.5 * track_change / RAD2DEG)  # NM
			if lead_distance > 20:  # NM
				lead_distance = 20  # NM
				turn_radius = lead_distance / np.tan(0.5 * track_change / RAD2DEG) # NM
				bank_angle = max(5, min(np.arctan(tas ** 2) / (G * turn_radius), max_angle))  # en degrés
		else :
			max_angle = 25  # en degrés
			bank_angle = max(5, min(0.5*track_change, max_angle))  # en degrés
			turn_radius = tas**2 / (G*np.tan(bank_angle / RAD2DEG)) / NM2M  # NM
			lead_distance = turn_radius * np.tan(0.5 * track_change / RAD2DEG)  # NM

		# Calcul de b_arc_starting_point et b_arc_ending_point : points de debut et fin de la transition en arc de cercle
		active_seg_norm = active_seg.norm()
		active_track = get_track(active_seg)  # en RAD
		next_track = get_track(next_seg)  # en RAD
		b_arc_starting_point = calcul_point_de_transition(a, active_seg_norm - lead_distance, active_track)
		b_arc_ending_point = calcul_point_de_transition(b, lead_distance,  next_track)

		# Calcul de l'angle a_b_bc_angle (A,B,BC) et du point b_arc_center_point (centre de l'arc de transition)
		bb_c = (turn_radius ** 2 + lead_distance ** 2) ** 0.5
		sens_virage = active_seg.det(next_seg)
		if sens_virage > 0:
			a_b_bc_angle = ((180 + track_change) / 2) / RAD2DEG  # en rad
			b_arc_center_point = g.Point(b.x - bb_c * np.sin((a_b_bc_angle-active_track)),
														b.y + bb_c * np.cos((a_b_bc_angle-active_track)))
			bank_angle = - bank_angle # en degrés
		else:
			a_b_bc_angle = ((180 - track_change) / 2) / RAD2DEG # en rad
			b_arc_center_point = g.Point(b.x + bb_c * np.sin((a_b_bc_angle-active_track)),
										b.y - bb_c * np.cos((a_b_bc_angle-active_track)))
	return [g.Arc(b_arc_center_point, b_arc_starting_point, b_arc_ending_point, turn_radius, lead_distance, bank_angle,
															track_change, sens_virage)]


def compute_transition_fly_over(active_seg, next_seg, tas):
	"""Calcul une transition fly_over entre deux legs
		- entrées : les deux legs en question (active_seg et next_seg) et la True Air Speed (tas)
		- sortie: liste contenant deux objets Arc et un objet Segment, ordonnés selon le sens de parcours """

	# Recuperation du point B (fin) du premier segment
	b = active_seg.end

	# Calcul du premier arc de cercle
	# Calcul du track change entre les deux segments
	track_change_initial = np.arccos((active_seg.scal(next_seg)) / (active_seg.norm() * next_seg.norm()))* RAD2DEG
	# Choix de l'angle d'intersection intersect_angle avec la prochaine leg (seg_next)
	if track_change_initial < 60:
		intersect_angle = track_change_initial/(3*RAD2DEG)  # en degrés
	else:
		intersect_angle = np.pi/6
	track_change = track_change_initial + intersect_angle*RAD2DEG

	# Si pas de virage :
	if track_change_initial < EPSILON:
		arc = g.Arc(b, b, b, 0, 0, 0, 0, 0)
		segment_jointif = g.Segment(b, b)
		return [arc, segment_jointif, arc]  # arc nul, segment nul et arc nul

	# si virage :
	# Identique fly by
	else:
		if ALTITUDE > 195:
			max_angle = (16 - 25) / (300 - 195) * (ALTITUDE - 195) + 25
			bank_angle = max(5, min(0.5 * track_change, max_angle))  # en DEG
			turn_radius = tas ** 2 / (G * np.tan(bank_angle / RAD2DEG)) / NM2M  # NM
			lead_distance = turn_radius * np.tan(0.5 * track_change / RAD2DEG)  # NM
			if lead_distance > 20:  # NM
				lead_distance = 20  # NM
				turn_radius = lead_distance / np.tan(0.5 * track_change / RAD2DEG)
				bank_angle = max(5, min(np.arctan(tas ** 2) / (G * turn_radius), max_angle))
		else :
			max_angle = 25  # DEG
			bank_angle = max(5, min(0.5*track_change, max_angle))  # DEG
			turn_radius = tas**2 / (G*np.tan(bank_angle / RAD2DEG)) / NM2M  # NM
			lead_distance = turn_radius * np.tan(0.5 * track_change / RAD2DEG)

	# on désigne par I1 le waypoint de calcul imaginaire du premier Arc (cf DFS)
		i1_arc_starting_point = b  # par construction, on commence la transition sur B
		active_track = get_track(active_seg)
		i1 = g.Point(b.x + lead_distance * np.sin(active_track),  # on place le waypoint imaginaire I1 à une
															b.y + lead_distance * np.cos(active_track))  # distance
		# lead_distance de B

		# Calcul de la track (next track_im) du segment I1I_2 à créer (next_seg_im) à partir de
		# La track de BC (next_track) et de l'angle d'intersection (intersect_angle)
		next_track = get_track(next_seg)

		# Pour faire en sorte que next_track_im appartienne à [-pi; pi]
		if active_seg.det(next_seg) > 0:
			if abs(next_track) < np.pi-intersect_angle:
				next_track_im = next_track - intersect_angle
			else:
				next_track_im = next_track - intersect_angle - np.sign(next_track)*2*np.pi
		else:
			if abs(next_track) < np.pi-intersect_angle:
				next_track_im = next_track + intersect_angle
			else:
				next_track_im = next_track + intersect_angle - np.sign(next_track)*2*np.pi

		next_seg_norm = next_seg.norm()

		# Création du segment next_seg_im qui part de I1 dans une direction next_track_im
		# La longueur du segment est fixée à 2 fois celle du prochain segment pour assurer l'intersection
		next_seg_im = g.Segment(i1, g.Point(i1.x + 2*next_seg_norm*np.sin(next_track_im),
																			i1.y + 2*next_seg_norm*np.cos(next_track_im)))

		i1_arc_ending_point = calcul_point_de_transition(i1, lead_distance, next_track_im)

		# Calcul de l'angle a_im1_im1_center et du point im1_center (centre de l'arc de transition)
		# Identique fonction fly by avec I1 = B et I1C = BC
		i1_i1c = (turn_radius ** 2 + lead_distance ** 2) ** 0.5  # distance entre le waypoint imaginaire et le centre
		# de la transition
		sens_virage = active_seg.det(next_seg_im)
		if sens_virage > 0:
			a_i1_i1c_angle = ((180 + track_change) / 2) / RAD2DEG  # en rad
			i1_center = g.Point(i1.x - i1_i1c * np.sin((a_i1_i1c_angle - active_track)),
												i1.y + i1_i1c * np.cos((a_i1_i1c_angle - active_track)))
			bank_angle = - bank_angle

		else:
			a_i1_i1c_angle = ((180 - track_change) / 2) / RAD2DEG
			i1_center = g.Point(i1.x + i1_i1c * np.sin((a_i1_i1c_angle - active_track)),
												i1.y - i1_i1c * np.cos((a_i1_i1c_angle - active_track)))

	# arc pour le wapoint imaginaire I1
	arc1 = g.Arc(i1_center, i1_arc_starting_point, i1_arc_ending_point, turn_radius, lead_distance, bank_angle, track_change, sens_virage)

	# try:   #try except à compléter lors de la mise en place de la gestion des discontinuités
	i2 = next_seg_im.intersection(next_seg)  # exception si pas d'intersection, sinon, le poitn d'intersection est I2
	seg_i1_i2 = g.Segment(i1, i2)
	seg_i2_next = g.Segment(i2, next_seg.end)  # segment de I2 vers le prochain waypoint (C)

	# calcul de la transition entre les segments I_1I_2 et I_2C
	arc2 = compute_transition_fly_by(seg_i1_i2, seg_i2_next, tas)[0]

	# calcul du segment entre les 2 arcs
	segment_jointif = g.Segment(arc1.end, arc2.start)

	# renvoi du premier arc sur I1, du segment entre les deux arcs et du second arc sur I2
	return [arc1, segment_jointif, arc2]
	# except Exception:


def get_track(segment):
	"""La route d'un segment est calculee en RAD, entre -pi et pi"""

	# construction segment vertical pour calculer la route.
	seg_calcul = g.Segment(segment.start, g.Point(segment.start.x, segment.start.y + 100))
	track = np.arccos(seg_calcul.scal(segment) / ((seg_calcul.norm())*(segment.norm())))

	# track positive pour un virage a droite
	if seg_calcul.det(segment) > 0:
		return -track  # en RAD
	else :
		return track  # en RAD


def calcul_point_de_transition(origine, dist, track):
	"""Permet de placer un point sur un segment donné, à une distance dist de son origine
	- entrées : origine et track du segment, dist
	- sortie : le point en question"""
	return g.Point(origine.x + dist * np.sin(track), origine.y + dist * np.cos(track))

