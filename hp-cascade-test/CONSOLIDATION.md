# CONSOLIDATION — Un seul fichier candidat (30 octobre 2026)

**Demande de Zackary : « essaie d'avoir un seul code pas 3 ».**
**Originaux intacts dans `workspace/user/files/` (SHA vérifiés). Ce
fichier unique est un CANDIDAT, pas un remplacement automatique.**

## Fichier produit

- `Tlog_v3_7_0_HP_uni_v1.py` — 7 427 lignes, SHA-256
  `45dadb940e6743c4b0f63475c1eb1ad5c2271c5d100ff11ca419f620cc73dc8c`,
  VERSION interne `v3.7.0-HP-uni-v1`.
- Construction (`build_uni.py`, mécanique, auditable) : v3.5.5 en base,
  v3.6.0 puis v3.7.0 appendés, blocs chargeurs `SourceFileLoader`
  supprimés, références `_v1_module.` / `_v2_module.` remplacées par
  les noms nus, `main()` intermédiaires renommés (`main_v1_legacy`,
  `main_v1`, `main_v2`), seul le `main()` v3.7.0 reste l'entrée
  `__main__`. Seule occurrence restante de `_v1_module.` /
  `_v2_module.` : une ligne du commentaire d'en-tête, pas du code.

## Vérification d'équivalence (`verify_uni.py`, `verification_uni.json`)

- `compute_5_threshold_cascade` sur la série V1 du test : sorties
  IDENTIQUES (chaîne vs unique).
- `analyze_noise_information_content` sur une série fixe (graine 0,
  200 points) : sorties IDENTIQUES.
- Présence vérifiée dans le fichier unique : `run_pipeline`,
  `decompress_energy_flux`, `detect_multi_thresholds`,
  `compute_time_aligned_progress`, `detect_order_saliency`,
  `fit_regime_attractor`, `predict_regime_attractor`,
  `complexity_guided_mc_paths`, `run_multilevel_v3`,
  `level_next_threshold_v3`, `compute_5_threshold_cascade`,
  `analyze_noise_information_content`, `main`, `main_v1`, `main_v2`.
- Syntaxe : `py_compile` OK.

## Limite dite

L'équivalence est vérifiée sur la cascade et le discriminateur bruit,
pas sur un lot complet (prédiction L1–L7 non re-testée dans le fichier
unique). Le fichier unique ne devient la référence que sur validation
de Zackary ; sinon la chaîne 3 fichiers reste la référence, et le test
cascade ci-joint porte sur la chaîne reçue, pas sur le candidat.
