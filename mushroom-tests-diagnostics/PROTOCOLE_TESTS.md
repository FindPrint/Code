# Protocole gelé — 3 tests diagnostics mushroom v3.4 (27 oct. 2026, avant tout run)

Demandé par l'utilisateur le 27 oct. 2026, dans cet ordre : (1) test
d'encodage, (2) nul propre, (3) corrélations entre flux dominants.
Ces tests sont des diagnostics du lot v3.4, pas une validation des
seuils : le découvreur ne valide jamais. Publication systématique :
GitHub (texte + figures + PDF, Release si > 25 Mo) et PDF, comme pour
le lot.

Pipeline commun : `Tlog_v3_4_harmonic_v3.py` SHA-256
`81092eb6…` (v3.4-H3, original v3.3-H1 intact), mode stable, w_size
initial 80, test cohen_d, graine 42, HARMONIC_PROB 0,45, sans
triangulation complète, contrôle exclu des flux, ordre des lignes
préservé, 2 runs en parallèle, design résumable (run avec
`run_summary.json` sauté, run partiel jeté et relancé de zéro).

## Test 1 — Encodage (alphabétique vs ordre d'apparition)

Données : même CSV brut Kaggle, encodage chaque lettre → entier par
ordre alphabétique de la lettre, par colonne
(`encodage/data/mushrooms_alpha.csv`, SHA-256
`4552be72…`, 8 124 × 23, 2 480 NaN, tous dans `stalk-root` pour `?`,
comme dans le lot). Mapping : `encodage/data/mapping_alpha.json`.
L'ordre alphabétique diffère de l'ordre d'apparition pour les 3
contrôles testés (vérifié avant le run) : class e=0,p=1 (apparition
p=0,e=1) ; odor a=0,c=1,f=2,l=3,m=4,n=5,p=6,s=7,y=8 (apparition
p=0,a=1,l=2,n=3,f=4,c=5,y=6,s=7,m=8) ; cap-surface f=0,g=1,s=2,y=3
(apparition s=0,y=1,f=2,g=3). Contrôles, dans l'ordre : class, odor,
cap-surface. Comparaison gelée avec le lot d'origine : seuil MC,
score MC, moyenne bootstrap. Règle : écart de seuil MC > 5 pts OU
écart de score MC > 0,05 → sensible à l'encodage (artefact
d'encodage probable) ; sinon, robuste à l'encodage pour ce contrôle.

## Test 2 — Nul propre (permutation du contrôle)

Données : encodage d'origine, colonne de contrôle permutée
indépendamment des flux avec `np.random.default_rng(1234)
.permutation` (graine gelée, permutation enregistrée), flux intacts,
fréquences marginales du contrôle conservées. Contrôles : class,
odor, cap-surface, mêmes paramètres. Comparaison gelée : score MC
nul vs score MC réel. Règle : score nul ≥ score réel − 0,05 →
le score réel n'est pas distinguable du nul (le seuil ne porte pas
d'association contrôle-flux mesurable) ; sinon, association
mesurable au-delà du nul. La position du seuil nul est rapportée
à titre descriptif seulement.

## Test 3 — Corrélations entre flux dominants (aucun run pipeline)

Données : codes bruts (lettres) et encodage d'origine. Mesures
gelées : Spearman sur les valeurs encodées + V de Cramér sur les
codes bruts, matrice complète 23 × 23, top 15 paires rapportées,
focus pré-enregistré sur le trio stalk-color-above-ring /
stalk-color-below-ring / ring-type, plus taux d'accord exact entre
les deux colonnes stalk-color. Interprétation gelée : une forte
corrélation entre deux flux ne prouve pas la circularité, elle
retire seulement l'indépendance de leurs témoignages.

## Hypothèses de l'utilisateur (non établies, à tester)

L'utilisateur propose : Q5 énorme partout = données en partie sans
flux réceptif ; Q4 plat partout = persistance de l'information dans
le dataset/flux ; Q2 centré sur veil-color = tension là où le signal
est placé sans flux physique/biologique. Ces lectures sont des
hypothèses, pas des conclusions du lot : les tests 1 et 2 séparent
« signal dans les données » de « signature du pipeline », le test 3
sépare « témoignages indépendants » de « flux qui se suivent ».
Aucune ne sera affirmée sans mesure.

## Limites (identiques au lot)

Codes nominaux, seuils = coupes de rang (plateaux), lecture
descriptive, aucune vérité terrain, jamais une règle
comestible/vénéneux. Aucun flux physique, biologique, chimique,
temporel ou spatial n'existe dans ce dataset (voir inventaire :
descripteurs morphologiques + odor + habitat + population + classe
e/p) ; le manque est structurel, pas un réglage.
