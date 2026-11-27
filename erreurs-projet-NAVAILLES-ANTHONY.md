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

## Erreur 4 : CrashLoopBackOff sur app-admin (HTTP 400 Bad Request sur livenessProbe)
- **Objectif :** Stabiliser les 3 réplicas de `deploy-admin-n-27-11-2026`.
- **Commande :** `kubectl logs -l app=app-admin-n-27-11-2026 -n ns-apps-n-27-11-2026`
- **Erreur :** `"GET / HTTP/1.1" 400 143 "-" "kube-probe/1.37"` suivi de `Handling signal: term`. Django rejetait l'IP interne du Pod envoyée par la sonde kubelet dans l'en-tête `Host`.
- **Résolution :** Ajout explicite de `ALLOWED_HOSTS = ['*']` à la fin de `apps/app-admin/core/settings.py`, rebuild/push de l'image et `kubectl rollout restart`.

---

## Erreur 4 : CrashLoopBackOff sur app-admin (HTTP 400 Bad Request sur livenessProbe)
- **Objectif :** Stabiliser les 3 réplicas de `deploy-admin-n-27-11-2026`.
- **Commande :** `kubectl logs -l app=app-admin-n-27-11-2026 -n ns-apps-n-27-11-2026`
- **Erreur :** `"GET / HTTP/1.1" 400 143 "-" "kube-probe/1.37"` suivi de `Handling signal: term`. Django rejetait l'IP interne du Pod envoyée par la sonde kubelet dans l'en-tête `Host`.
- **Résolution :** Ajout explicite de `ALLOWED_HOSTS = ['*']` à la fin de `apps/app-admin/core/settings.py`, rebuild/push de l'image et `kubectl rollout restart`.

---

## Erreur 5 : Redirection /login et fichiers /static en 404 derrière Envoy Gateway
- **Objectif :** Afficher l'interface complète d'administration Django via la route `/admin`.
- **Erreur :** HTTP 404 sur `/login/?next=/` puis chargement sans CSS sur `/static/...`, car Envoy dirigeait ces préfixes vers la route racine `/` (`app-stripe`).
- **Résolution :** Ajout des règles `PathPrefix` pour `/login` et `/static` dans `route-admin-n-27-11-2026` (`manifests/05-gateway.yaml`).

---
