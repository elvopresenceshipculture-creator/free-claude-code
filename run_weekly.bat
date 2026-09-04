@echo off
chcp 65001 >nul
cd /d C:\Users\HP\free-claude-code
echo Analyse de votre feuille de calcul Excel et generation du rapport hebdomadaire...
uv run python weekly_progress_reporter.py
echo.
echo Rapport hebdomadaire envoye sur Discord avec succes !
pause
