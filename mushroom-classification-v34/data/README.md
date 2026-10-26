# Data / Données

Source: Kaggle dataset `uciml/mushroom-classification`
https://www.kaggle.com/datasets/uciml/mushroom-classification

- Downloaded zip: `mushroom-classification.zip` (35,057 bytes),
  SHA-256 `4e688bc1234b8f56d5abcbafc64f50983465066dd0036082714ff911c0a35081`
  (zip not included here: binary archives are excluded from snapshot
  pushes; download it from Kaggle and verify the hash).
- Original CSV in the zip: `mushrooms.csv` (374,003 bytes),
  SHA-256 `f0284c7a4210c4b0793713de9c45841d66f9bb27f6408f8bfedb6b34e6d6f53c`
  — included here as `raw/mushrooms.csv`.
- Working file: `mushrooms_pipeline.csv` (8,124 × 23, numeric),
  SHA-256 `fa6e5cebe8e26faaa803873c7cd01f9d9f4c6b9bafe2884270572a0002fda0ee`.
- Encoding: each letter → integer by order of first appearance, per
  column; see `mapping_encodage.json`. `?` in `stalk-root` (2,480 rows)
  is true missing (NaN), not a category. `veil-type` is constant.
- The zip contains a SINGLE CSV, so the "merge" is trivial: no other
  file to join, no row added or removed.

Source : dataset Kaggle `uciml/mushroom-classification`.
Le zip contient UN SEUL CSV, donc la « fusion » est triviale.
