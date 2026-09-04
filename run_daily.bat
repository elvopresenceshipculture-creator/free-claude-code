@echo off
chcp 65001 >nul
cd /d C:\Users\HP\free-claude-code
echo Lancement du briefing matinal (Biomédical, Bourses & IA)...
uv run python scholarship_fetcher.py
echo.
echo Termine !
pause
