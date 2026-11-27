# Code — UNIVERSAL_LOG v6.2.0

**Dépôt public depuis le 19 novembre 2026, par décision de Zackary
Drasse-Ménard. Le pipeline n'est jamais vendu, jamais commercialisé
sous aucune forme.**

## Fichiers

| Fichier | Contenu |
|---|---|
| `universal_v6.2.0_cohen.py` | Pipeline UNIVERSAL_LOG v6.2.0-L7aL7b-CohenD — version de travail (adoptée le 19 nov. 2026) |
| `universal_v6.1.0_cohen.py` | Pipeline UNIVERSAL_LOG v6.1.0-L7aL7b-CohenD — version de référence (adoptée le 16 nov. 2026 à 18h34) |
| `universal_v6.0.0_cohen.py` | Pipeline UNIVERSAL_LOG v6.0.0-L7aL7b-CohenD — référence intacte |
| `build_v6.1.py` | Script de construction de la v6.1 depuis la v6.0.0 |
| `build_v6.py` | Script de construction de la v6.0 |
| `README.md` | Ce fichier |

## Version

- **Version de travail :** v6.2.0-L7aL7b-CohenD
- **SHA-256 :** `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
- **Taille :** 624 157 octets, 13 033 lignes
- **Référence :** v6.1.0-L7aL7b-CohenD (SHA-256
  `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9`),
  623 495 octets, 13 022 lignes.
- **Référence intacte :** v6.0.0-L7aL7b-CohenD (SHA-256
  `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`),
  conservée dans l'historique de ce dépôt.
- **Original v5.9.0f intact** (SHA-256
  `4f80f6a7d0809e802cbc9ec30c0bed552c1c8a95eb58687fd78e4ffd8e808260`),
  fourni par Zackary Drasse-Ménard, jamais modifié.

## Ce qui change dans la v6.2 par rapport à la v6.1

- **Graine L5 déterministe :** la graine Monte Carlo L5 utilise
  désormais un hachage stable (SHA-256 du nom de la métrique) au lieu
  de `hash(metric)` de Python, dont la valeur change à chaque
  processus. Gigue L5 mesurée : 0,0000 (re-confirmée à froid, §8.50
  et §8.77 du livre blanc PDAC). Les cascades sont identiques à la
  v6.1 (S_sep v6.2 = S_sep v6.1 exactement sur 29/29 paires, §8.38).
  Aucun autre changement : estimateurs, seuils, Cohen-d inchangés.

## Ce qui change par rapport à la v6.0.0

- **Correctif L7a :** le vote L7a ne retourne plus un faux « up » à
  confiance 0,500 sur les petites séries (n < 75) — les poids non finis
  sont neutralisés et le vote devient « indéterminé » quand il n'y a
  rien à voter. Validé sur 10 runs : cascades identiques à la v6 sur
  HP35 et TCGA v4 ; votes L7a finis sur les 5 petites cohortes.
- **Minimum fast : 50 → 40 points** (pour les 45 lignées CRISPR DepMap).
  Le reste (estimateurs, cascades, seuils, Cohen-d) est inchangé.

## Ce qui change par rapport à la v5.9.0f

Cohen-d partout, Cliff retiré (modes robust/full/predict et comparaison
inter-classes). Raison notée dans l'en-tête du fichier.

## Preuve Cohen contre Cliff (14 novembre 2026)

Comparaison proposée par Zackary, complète : **4 comparaisons sur 4,
cascades identiques** (original 0/16/90/376 ; nul 0/204/273/735 ;
no5ns 0/225/462/786 ; HP35). Cliff fast ≈ 45 min contre Cohen fast
≈ 4 min (environ 11× plus lent). Vérification v6 sur HP35 (run fast,
~4 min) : cascade identique 0/16/90/376.

## Mode d'emploi (fast)

```bash
python3 universal_v6.2.0_cohen.py \
  --input flux.csv --output results_fast \
  --mode fast --control_col step --target_col <colonne-cible>
```

- **Mode fast** = cohen_d, 12 itérations Monte Carlo, ~4 minutes.
- **Minimum : 40 points par série** (`min_len` 40, `w_size` 80).
  En dessous, le pipeline refuse (`Série trop courte`).
- Le pipeline est **aveugle** : il ne voit jamais la température physique
  ni la vérité terrain. L'ordre des lignes est la seule information
  d'ordonnancement. Toute traduction en température ou comparaison à une
  valeur critique se fait après le run, dans le harnais, sans retour dans
  les paramètres.

## Travail qui utilise ce pipeline

Projet PDAC v6 (cancer du pancréas, ARN / protéine / CRISPR) :
livre blanc public [FindPrint/tlogNext-cancer-pdac](https://github.com/FindPrint/tlogNext-cancer-pdac)
(sections §8.1 à §8.98, PDF 1 447 pages), et dépôt
[FindPrint/pancreatic-cancer-open-data-reproducibility](https://github.com/FindPrint/pancreatic-cancer-open-data-reproducibility)
(livre blanc §8.30–§8.36, scripts, provenances, résultats).
