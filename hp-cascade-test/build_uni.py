# -*- coding: utf-8 -*-
"""Construit le fichier unique Tlog_v3_7_0_HP_uni_v1.py à partir des
3 fichiers reçus, SANS modifier les originaux.
Méthode : v3.5.5 en base, puis v3.6.0 et v3.7.0 appendés avec leurs
blocs chargeurs supprimés et leurs références _v1_module./_v2_module.
remplacées par les noms nus (les définitions sont alors au même niveau).
Les main() intermédiaires sont renommés ; seul le main() v3.7.0 reste
l'entrée __main__. VERSION finale = v3.7.0-HP-uni-v1 (provenance, pas
comportement : la vérification d'équivalence compare les sorties).
"""
from pathlib import Path

USER_FILES = Path.home() / "workspace" / "user" / "files"
OUT = Path(__file__).resolve().parent


def strip_main_block(text):
    marker = 'if __name__ == "__main__":'
    idx = text.find(marker)
    assert idx != -1, "bloc __main__ introuvable"
    return text[:idx].rstrip() + "\n"


def cut_loader(text, start_marker, end_marker):
    i = text.find(start_marker)
    j = text.find(end_marker)
    assert i != -1 and j != -1, f"chargeur introuvable : {start_marker}"
    j_end = text.find("\n", j)
    return text[:i] + text[j_end + 1:]


v1 = (USER_FILES / "Tlog_v3_5_5_HP_v1.py").read_text(encoding="utf-8")
v1 = strip_main_block(v1)
# v3.5.5 définit main() deux fois (la 2e écrase la 1re) : on renomme.
v1 = v1.replace("def main():", "def main_v1_legacy():", 1)
v1 = v1.replace("def main():", "def main_v1():", 1)
assert "def main():" not in v1

v2 = (USER_FILES / "Tlog_v3_6_0_HP_v2.py").read_text(encoding="utf-8")
v2 = strip_main_block(v2)
v2 = cut_loader(v2, "# Re-use core analysis from v3.5.5-HP-v1",
                "ALL_METRICS = _v1_module.ALL_METRICS")
v2 = v2.replace("def main():", "def main_v2():", 1)
v2 = v2.replace("_v1_module.", "")
assert "_v1_module." not in v2

v3 = (USER_FILES / "Tlog_v3_7_0_HP_v3.py").read_text(encoding="utf-8")
# v3 : on garde son bloc __main__ (entrée finale).
v3 = cut_loader(v3, "# Re-use v3.6.0-HP-v2 logic",
                "get_domain_target_semantic_direction = _v2_module.get_domain_target_semantic_direction")
v3 = v3.replace("_v2_module.", "").replace("_v1_module.", "")
assert "_v2_module." not in v3 and "_v1_module." not in v3

header = '''# -*- coding: utf-8 -*-
"""
UNIVERSAL_LOG v3.7.0-HP-uni-v1 — Fichier unique consolidé (CANDIDAT)
=====================================================================
Construit le 30 octobre 2026 par assemblage mécanique des 3 fichiers reçus,
SANS modifier les originaux (workspace/user/files/, SHA vérifiés) :
- Tlog_v3_5_5_HP_v1.py (SHA 24e65495...)
- Tlog_v3_6_0_HP_v2.py (SHA 7a694848...)
- Tlog_v3_7_0_HP_v3.py (SHA 8527b92c...)
Méthode : v3.5.5 en base, v3.6.0 puis v3.7.0 appendés, blocs chargeurs
SourceFileLoader supprimés, références _v1_module./_v2_module. remplacées
par les noms nus, main() intermédiaires renommés (main_v1_legacy,
main_v1, main_v2), seul le main() v3.7.0 reste l'entrée __main__.
Ce fichier est un CANDIDAT : il ne remplace la chaîne 3 fichiers que si
la vérification d'équivalence (verify_uni.py) passe. Sinon, la chaîne
reçue reste la référence.
"""

'''

uni = header + v1 + "\n# ===== v3.6.0-HP-v2 (inliné) =====\n" + v2
uni += "\n# ===== v3.7.0-HP-v3 (inliné) =====\n" + v3
uni += '\nVERSION = "v3.7.0-HP-uni-v1"\n'

out_path = OUT / "Tlog_v3_7_0_HP_uni_v1.py"
out_path.write_text(uni, encoding="utf-8")
print(f"Écrit : {out_path} ({len(uni.splitlines())} lignes)")
