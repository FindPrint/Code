# Traceability rule — systematic, for every project with Muse
# Règle de traçabilité — systématique, pour tout projet avec Muse

**Decided 26 Oct 2026 by the author (Zackary), after the mushroom v3.4
repository: this pattern applies to ALL code, executions and projects
done with Muse, not just this lot. This file is the template.**

## EN — The rule

For every project, execution or code change with Muse, the following
must be archived, in the workspace AND in a (private by default) GitHub
repository, as memory and proof:

1. **Frozen protocol BEFORE any run** — question, settings, seeds,
   inclusion/exclusion rules, failure rules, interpretation limits.
   No silent change after runs start; any change is a new version.
2. **Code, versioned, with hash** — the exact file(s) used, SHA-256
   recorded in the protocol and in the README. Modified code is a new
   file/version, never an overwrite of the reference.
3. **Data, with source and hash** — origin URL, downloaded file hash,
   working file hash, row/column inventory, encoding/mapping, missing
   values. If data cannot be redistributed, archive the download
   script + hashes + a small sample, not the full file, and say so.
4. **Per-run outputs, complete** — run summaries, curves, tables,
   figures, logs, errors. An interrupted run is discarded and
   relaunched, never counted; its empty folder is not a result.
5. **Synthesis, verified, not summarised away** — full per-item detail
   (here: every threshold on every flux, F1/F2 before and after),
   with checks (stability vs bootstrap mean, fallback warnings).
6. **Final deliverable** — complete PDF/report + archive zip, built
   from verified synthesis files only, with figures included.
7. **Repository updates at checkpoints and at completion** — initial
   commit (code + protocol + data + verification), checkpoint commits
   (each completed run or batch of runs), final commit (synthesis +
   PDF + report). Commit messages state what changed and what is
   still running. Large binaries (PDF/zip > a few MB) go as GitHub
   Release assets when they exceed the snapshot push limit, with the
   release link recorded in the README.
8. **Bilingual documentation** — README and protocol in French and
   English; code in French (reference) + English copy for the parts
   peers need most, with logic verified identical.
9. **Corrections, transparent** — a bug found by verification is
   recorded (what, why, fix, re-verification), the affected runs are
   restarted, and the old version is kept for comparison, not deleted
   silently.
10. **Privacy by default** — repositories are PRIVATE. Peers access by
    invitation. Public visibility, and any licence choice, require the
    author's explicit per-project decision. The pipeline itself is
    never sold or commercialised; sharing for peer review/testing is
    not a sale, and the licence note must say so.

## FR — La règle

Pour tout projet, exécution ou modification de code avec Muse, les
éléments suivants doivent être archivés, dans le workspace ET dans un
dépôt GitHub (privé par défaut), comme mémoire et preuve :

1. **Protocole gelé AVANT tout run** — question, réglages, graines,
   règles d'inclusion/exclusion, règles d'échec, limites
   d'interprétation. Aucun changement silencieux après le début des
   runs ; tout changement = nouvelle version.
2. **Code versionné, avec empreinte** — le(s) fichier(s) exact(s)
   utilisé(s), SHA-256 dans le protocole et dans le README. Un code
   modifié est un nouveau fichier/version, jamais un écrasement de la
   référence.
3. **Données, avec source et empreinte** — URL d'origine, empreinte du
   fichier téléchargé, empreinte du fichier de travail, inventaire
   lignes/colonnes, encodage/mapping, valeurs manquantes. Si les données
   ne peuvent pas être redistribuées, archiver le script de
   téléchargement + les empreintes + un petit échantillon, pas le
   fichier complet, et le dire.
4. **Sorties par run, complètes** — résumés, courbes, tableaux,
   figures, logs, erreurs. Un run interrompu est jeté et relancé,
   jamais compté ; son dossier vide n'est pas un résultat.
5. **Synthèse vérifiée, pas résumée à l'excès** — détail complet par
   élément (ici : chaque seuil sur chaque flux, F1/F2 avant et après),
   avec vérifications (stabilité vs moyenne bootstrap, alertes de repli).
6. **Livrable final** — PDF/rapport complet + zip d'archive, construits
   uniquement à partir des fichiers de synthèse vérifiés, figures incluses.
7. **Mises à jour du dépôt aux points d'étape et à la fin** — commit
   initial (code + protocole + données + vérifications), commits de
   point d'étape (chaque run ou lot de runs terminés), commit final
   (synthèse + PDF + rapport). Les messages de commit disent ce qui a
   changé et ce qui tourne encore. Les gros binaires (PDF/zip de
   plusieurs Mo) passent en Release GitHub quand ils dépassent la limite
   du push par snapshot, avec le lien de release dans le README.
8. **Documentation bilingue** — README et protocole en français et en
   anglais ; code en français (référence) + copie anglaise pour les
   parties dont les pairs ont le plus besoin, logique vérifiée identique.
9. **Corrections transparentes** — un bug trouvé par vérification est
   consigné (quoi, pourquoi, correctif, re-vérification), les runs
   touchés sont relancés, et l'ancienne version est conservée pour
   comparaison, pas supprimée en silence.
10. **Confidentialité par défaut** — dépôts PRIVÉS. Accès des pairs par
    invitation. Visibilité publique, et tout choix de licence, exigent
    la décision explicite de l'auteur par projet. Le pipeline lui-même
    n'est jamais vendu ni commercialisé ; le partage pour relecture/test
    par les pairs n'est pas une vente, et la note de licence doit le dire.

## Template — minimal repository for a new project / Dépôt minimal pour un nouveau projet

```
pipeline/   <code>.py  (+ <code>_en.py if applicable)
data/       README (source + hashes) + working file or download script
docs/       PROTOCOL.md + PROTOCOLE.md + VERIFICATION.md + TRACEABILITY.md
scripts/    run_one.py + batch.sh + synthese.py (+ demo.py for quick test)
results/    README (status) + per-run outputs as they complete
README.md + README.fr.md + requirements.txt + LICENSE-NOTE.md
```

## Retroactive application / Application rétroactive

Projects completed before 26 Oct 2026 (breast cancer, food costs, air
quality, USGS, earthquake/tsunami, controls batch, etc.) have local
workspace archives (protocols, PDFs, zips) but no GitHub repository yet.
They will be backfilled into repositories on the author's request,
most recent first, following the same template — not silently, and not
all at once. Forward projects follow the rule from the start.
