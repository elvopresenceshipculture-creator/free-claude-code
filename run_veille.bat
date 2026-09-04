@echo off
chcp 65001 >nul
cd /d C:\Users\HP\free-claude-code
echo Lancement de la veille des bourses d'études académiques...
uv run python scholarship_fetcher.py
echo.
echo Operation terminee. Rapport sauvegarde dans C:\Users\HP\free-claude-code\scholarships\
pause
