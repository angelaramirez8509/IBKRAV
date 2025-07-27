#!/bin/bash

echo '🔎 Ejecutando pruebas con Pytest...'
source .venv/bin/activate

pytest tests/ --tb=short --disable-warnings --maxfail=5 | tee test_report.txt




echo ''
echo '📋 Resumen de resultados:'
grep -E 'passed|failed|error' test_report.txt | tail -n 3
