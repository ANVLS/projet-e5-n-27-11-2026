# Journal des erreurs et résolutions - Projet E5 Kubernetes
**Candidat :** Anthony NAVAILLES | **Empreinte :** `n-27-11-2026`

## Erreur 1 : Ressources CPU insuffisantes au démarrage de Minikube
* **Objectif :** Démarrer le cluster Minikube local.
* **Commande :** `minikube start`
* **Erreur :** `Exiting due to RSRC_INSUFFICIENT_CORES: has less than 2 CPUs available, but Kubernetes requires at least 2 to be available`
* **Résolution :** Augmentation de la configuration matérielle de la VM `LabTeste` à 2 vCPU minimum avant de relancer le cluster.

## Erreur 2 : Fichier de configuration Minikube corrompu après arrêt
* **Objectif :** Démarrer le cluster Minikube avec le driver Docker.
* **Commande :** `minikube start --driver=docker`
* **Erreur :** `Exiting due to HOST_CONFIG_LOAD: Unable to load config: unmarshal: unexpected end of JSON input`
* **Résolution :** Purge complète des profils locaux (`minikube delete --all --purge && rm -rf ~/.minikube ~/.kube`) puis redémarrage propre du cluster.

---
