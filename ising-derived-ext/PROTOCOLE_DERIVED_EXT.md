# Protocole GELÉ — Extension dérivés : factoriel complet + famille rollmean + nuls

**Gel : 28 octobre 2026, avant construction et avant runs. Demande utilisateur
(28 oct. 2026, 12:58 EDT) : « ajouter maintenant tout les autres fluxs
monotone en plus comme energy magnétisation localvar ect et autre fluxs de
d'autre famille monotone ». Ce protocole étend le lot `ising-derived`
(PROTOCOLE_DERIVED.md, 11 runs, terminé 12:32 EDT) sans le modifier :
les 11 runs du lot 1 restent intacts, leurs sorties sont réutilisées
(paysages des 3 nuls poolés pour R3).**

## Portée gelée : 12 nouveaux runs

**Bases monotones** (Spearman vs T mesuré descriptivement sur les snapshots,
T lue uniquement pour cette description, jamais dans la construction) :
`fliprate` +0,9986, `energy` +0,9787, `magnetization` −0,8758,
`localvar` +0,9770. `susceptibility` +0,3860 : NON monotone, exclue comme
base (reste flux analysé, comme au lot 1).

**Complétion du factoriel (4)** — constructions existantes × bases manquantes :
- `expmean_fliprate`, `expmean_localvar` (moyenne expansive par bloc)
- `rollvar_fliprate_40`, `rollvar_localvar_40` (variance glissante, fenêtre 40)

**Nouvelle famille rollmean (4)** — moyenne glissante, pendant premier-moment
de rollvar, fenêtre 40, sans réinitialisation :
- `rollmean_energy_40`, `rollmean_magnetization_40`, `rollmean_fliprate_40`,
  `rollmean_localvar_40`

**Nuls (4)** — permutation `default_rng(1234)` de la série entière
(même permutation d'indices que le lot 1, marginales différentes) :
- `null_expmean_fliprate`, `null_rollvar_fliprate`, `null_rollmean_mag`,
  `null_rollmean_localvar`

**Total : 12 runs.** Analysés fixés aux 6 originaux (χ incluse, jamais
contrôle), mêmes paramètres pipeline que le lot 1 (v3.5.4-H1, mode stable,
w80, cohen_d, graine 42, HARMONIC_PROB 0,45, Theiler 1/φ planché source fixe),
max 2 en parallèle, reprise sur `run_summary.json`.

## Exclusions nommées (avec raison mesurée, pas d'arbitraire)

- `flip` (toutes constructions) : `flip` = 1024 × `fliprate` EXACTEMENT
  (vérifié) → rangs identiques → seuils identiques par construction.
  Redondance déjà établie (lot 1 : seuils bit-identiques).
- `susceptibility` comme base : non monotone (Spearman +0,3860, pic à Tc).
- `expstd` / `rollstd` (racine des variances) : transformée monotone de
  expvar/rollvar → rangs identiques (Spearman 1,0 mesuré) → seuils identiques.
- Autres fenêtres (20/80) : variation de paramètre, pas une nouvelle famille
  — hors de ce lot (lot de robustesse éventuel, séparé).
- Normalisation type χ (Var/T) : exigerait T dans la construction —
  interdite par la règle de cécité.

## Construction (sans T)

Nouveau fichier `data/ising_derived_ext.csv` = les 17 colonnes du lot 1
**bit-identiques** + 12 nouvelles colonnes (8 dérivées + 4 nulls),
960 lignes. Le constructeur `gen_derived_ext.py` ne lit QUE
`data/ising_derived.csv` (une seule lecture CSV ; aucune référence au
fichier température). Blocs = 24 blocs de 40 lignes consécutives (position).
Formules gelées, identiques au lot 1 pour expmean/rollvar :
- `expmean_<X>` : moyenne expansive par bloc, réinitialisée à chaque bloc.
- `rollvar_<X>_40` : variance glissante arrière, fenêtre 40, min_periods=1,
  ddof=1, sans réinitialisation, première valeur → 0,0.
- `rollmean_<X>_40` : moyenne glissante arrière, fenêtre 40, min_periods=1,
  sans réinitialisation (première valeur = X[0]).

## Portes E1–E7 (avant runs, construction bloquée sinon)

- E1 : 960 lignes × 29 colonnes, 0 NaN.
- E2 : les 17 premières colonnes bit-identiques à `ising_derived.csv`.
- E3 : rollvar/rollmean sans réinitialisation (la valeur à l'indice 40
  utilise la fenêtre [1..40], pas un redémarrage).
- E4 : expmean réinitialisée par bloc (valeur à l'indice 40 = X[40]).
- E5 : les 4 nuls = permutations exactes (tri identique) de leur colonne source.
- E6 : le constructeur ne lit jamais le fichier température (revue de code +
  aucune colonne température dans le CSV produit).
- E7 : vérification des exclusions — Spearman(flip, fliprate) = 1 et
  flip = 1024·fliprate ; Spearman(expvar, √expvar) = 1.

## Règles de lecture R1–R5 (reprises du lot 1, sans changement)

- **R1** : candidat deuxième seuil = groupe de pics forts (rel ≥ 0,90)
  séparé de ≥ 0,20 du groupe principal, présent dans ≥ 2 runs à contrôles
  dérivés, ET absent dans les runs nuls correspondants (7 nuls poolés :
  3 du lot 1 + 4 nouveaux).
- **R2** (généralisée) : présent sous construction expansive mais absent
  sous construction glissante de la MÊME base et de la MÊME famille
  (expvar↔rollvar, expmean↔rollmean) → artefact de mémoire. Pour un
  candidat trouvé sous contrôle glissant, R2 = non applicable (mémoire
  déjà retirée) — rapporté tel quel.
- **R3** : présent dans un run nul à la même T → artefact de machinerie.
- **R4** : candidat réel = survit à R1+R2+R3 ET à T séparée de ≥ 0,20
  du groupe Tc → à confirmer par L=64 + 2e graine (hors lot).
- **R5** : tout est rapporté, aucun paramètre touché après les résultats.

## Sorties

Harnais `run_one_derived_ext.py` (copie de `run_one_derived.py`, seuls les
chemins changent : dataset étendu, sorties `runs_ext/<controle>/`).
Synthèse `synthese_derived_ext.py` (mêmes vérifications : traduction T
recalculée, exclusion du contrôle, identité flip/fliprate ; paysages des
nuls du lot 1 poolés pour R3). Rapport `RAPPORT_DERIVED_EXT.md`, puis
PDF + zip + publication GitHub complète (dossier `ising-derived/` existant,
sous-dossier `runs_ext/` ; figures préfixées).
