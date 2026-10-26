# Protocole gelé AVANT le run — pipeline v3.3 sur Ashkin-Teller (22 oct. 2026)

- Entrée : `at_fluxes.csv` (1 224 lignes, 6 flux) — AUCUNE colonne température.
- Pipeline : `pipeline_autonome_v3_3_fixed.py` tel quel, mode stable,
  contrôle = `energy` (aussi flux), w_size 80, cohen_d, graine 42.
- Seuils attendus (vérité terrain du générateur, mesurée le 22 oct.) :
  - **Seuil 1 (spin)** : chute de magnetization_s à T≈4,6–4,9
    → fenêtre de hit : **50–60 %** de l'axe de progression.
  - **Seuil 2 (produit)** : chute de magnetization_prod à T≈5,2–5,6
    → fenêtre de hit : **62–73 %**.
- Verdict :
  - Le seuil principal (MC et défaut) tombe dans une des deux fenêtres = hit
    sur ce seuil ; on nomme lequel.
  - Paysage : un maximum local de la courbe de scan, hors ±5 pts du seuil
    principal, qui tombe dans l'AUTRE fenêtre = le second seuil est visible
    dans le paysage. Sinon : non visible.
  - Mapping seuil % → T : températures des lignes autour de la frontière
    de rang d'énergie (même méthode que le test Ising du 17 oct.).
- Rapport exigé (règle du 18 oct.) : seuils sur TOUS les flux, dérivés
  F1/F2 après seuil, seuils critiques attendus formulés explicitement.
