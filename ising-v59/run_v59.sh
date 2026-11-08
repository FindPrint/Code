#!/bin/bash
set -u
bash run_synth59.sh
bash run_ising59.sh
echo "$(date -Is) V59 DONE" | tee -a ising/run.log
