Projet E5 - Infrastructure E-Commerce Haute Disponibilite sous Kubernetes

Contexte et objectif
Pour repondre au besoin d'un site e-commerce generant 7 millions d'euros de chiffre d'affaires annuel qui ne peut se permettre aucune coupure de service, 
nous avons mis en place une infrastructure resiliente sous Kubernetes (via Minikube) sur une VM Debian.

Ce que nous avons mis en place
Conteneurisation securisee : Preparation de trois applications (boutique de paiement Stripe, administration Django et portail Flask) avec des images Docker multi-stage legeres, executees sans droits administrateur (non-root) et hebergees sur un registre prive local (localhost:5000).
Haute disponibilite (9 Pods) : Deploiement de chaque application en 3 exemplaires, surveilles par des sondes de sante (livenessProbe et readinessProbe). Si un conteneur plante, les autres prennent le relais pendant que Kubernetes le relance automatiquement.
Cloisonnement et securite : Separation en 2 Namespaces (ns-gateway-n-27-11-2026 et ns-apps-n-27-11-2026) pour isoler le paiement critique, gestion des cles API via des Secrets Kubernetes (exclus de GitHub), et exposition interne uniquement via ClusterIP.
Routage unique : Utilisation d'Envoy Gateway (Gateway API) comme porte d'entree unique pour aiguiller le trafic vers /, /admin et /front tout en repartissant la charge.

Livrables et suivi
apps/ : Codes sources et Dockerfile optimises.
manifests/ : Fichiers YAML declaratifs du cluster.
logs/ : Export de l'etat final des 9 Pods et historique complet des commandes.
erreurs-projet-NAVAILLES-ANTHONY.md : Suivi detaille des incidents rencontres et resolus.
