#!/usr/bin/env python3
"""Chronometre une commande (argv) et imprime la duree murale en secondes."""
import subprocess, sys, time
t0 = time.monotonic()
rc = subprocess.run(sys.argv[1:]).returncode
print(f"[TIMING] wall={time.monotonic() - t0:.1f}s rc={rc}", flush=True)
sys.exit(rc)
