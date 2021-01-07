Pour lancer l'application SANS le bus Ivy :
   - USE_IVY --> False
   - Lancer le main

Attention : quand l'animation prend fin, la fenêtre freeze puis se ferme.
	    Ce problème n'a pas été résolu car mineur étant donné que d'une
	    manière nominale, on doit utiliser le bus Ivy


Pour lancer l'application AVEC le bus Ivy :
- télécharger le module ivy.std_api
- télécharger ivyprobe si besoin (pour visualiser le bus)
disponible pour Windows sur https://www.eei.cena.fr/products/ivy/download/binaries.html#windows 
- faire dans cet ordre :
	USE_IVy --> True
	Lancer le main.py --> lance le ND
	Attendre 2s
	Lancer testIvyLEGS.py --> lance le programme simulant l'envoi des Legs par le groupe LEGS
	Attendre 1s
	Lancer testIvySEQ.py --> lance le programme simulant l'envoi de données de la part du groupe SEQ
	Attendre 1s
	Lancer testIvySIMU.py --> lance le programme simulant l'envoi de données du simulateur


Attention : quelquefois, des problèmes peuvent apparaître dans le calcul de la trajectoire. 
            La seule manière de continuer la simulation et de relancer la console...
