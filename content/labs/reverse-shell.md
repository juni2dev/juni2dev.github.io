+++
title = "splunk"
date = 2026-05-12
tags = ["splunk"]
draft = true
toc = true
description = "splunk"
+++

Déploiement d’instance sur Splunk

Splunk offre la possibilité d’adapter le déploiement en fonction de nos exigences ainsi, on peut soit faire endosser toute la gestion à une seule instance on parle de « single-instance » ou bien distribuer notre déploiement en plusieurs instances auxquelles on spécifiera une fonction bien déterminée. D’un autre point de vue, l’aspect taille de l’infrastructure à monitorer peut aiguiller le choix d’un mode au détriment d’un autre.

Trois interrogations sont à prendre pour un choix pertinent :
- La taille de l’infrastructure et la complexité des données à manipuler.
- La diversité des sources (où les données proviennent).
- La huate disponibilité et la reprise après désastre en effectuant des réplications multi-sites

----------------------------------------------------------------------------------------------------------------------
La prochaine étape dans cette installation en instance unique (sigle-instance) consiste à configurer le receveur (l’indexer à proprement parler).