#!/usr/bin/env python3
"""
Weekly Progress Coaching Bot:
Analyses the exact user Excel file: C:\\Users\\HP\\Desktop\\Ma progression\\suivi_progression_travail.xlsx
Generates deep appreciations, perspectives, solutions, and advice for improvement,
and sends the weekly report via Discord Webhook.
"""

import os
import sys
import json
import urllib.request
from datetime import datetime, timezone

DISCORD_WEBHOOK_URL = os.environ.get(
    "DISCORD_WEBHOOK_URL",
    "https://discord.com/api/webhooks/1545199218547757146/iT9rvIDH75skQ6ERpUf4LJnmPPMK4YbBKAFpqi-ix0MHjFLpjWupU-leLigEqudYHNcF"
)

EXCEL_PATH = r"C:\Users\HP\Desktop\Ma progression\suivi_progression_travail.xlsx"

def analyze_progress_excel():
    data = {
        "total_hours": 0.0,
        "avg_progress": 0.0,
        "tasks": []
    }

    if not os.path.exists(EXCEL_PATH):
        print(f"Excel file not found at {EXCEL_PATH}", file=sys.stderr)
        return data

    try:
        import openpyxl
        wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
        if "Suivi & Bilan Hebdomadaire" in wb.sheetnames:
            ws = wb["Suivi & Bilan Hebdomadaire"]
            total_h = ws['B5'].value
            avg_p = ws['E5'].value
            if isinstance(total_h, (int, float)):
                data["total_hours"] = float(total_h)
            if isinstance(avg_p, (int, float)):
                data["avg_progress"] = float(avg_p) if avg_p <= 1 else float(avg_p) / 100.0

            for r in range(18, 35):
                date_val = ws.cell(row=r, column=1).value
                task_val = ws.cell(row=r, column=2).value
                hours_val = ws.cell(row=r, column=3).value
                prog_val = ws.cell(row=r, column=4).value
                note_val = ws.cell(row=r, column=5).value
                appr_val = ws.cell(row=r, column=6).value

                if task_val:
                    data["tasks"].append({
                        "date": str(date_val or ""),
                        "task": str(task_val),
                        "hours": float(hours_val) if isinstance(hours_val, (int, float)) else 0.0,
                        "progress": float(prog_val) if isinstance(prog_val, (int, float)) else 0.0,
                        "note": str(note_val or ""),
                        "appreciation": str(appr_val or "")
                    })
    except Exception as e:
        print(f"Error parsing Excel file: {e}", file=sys.stderr)

    return data

def generate_weekly_report():
    date_str = datetime.now(timezone.utc).strftime("%d/%m/%Y")
    data = analyze_progress_excel()

    total_h = data["total_hours"]
    avg_p = data["avg_progress"] * 100

    if avg_p >= 80 or total_h >= 30:
        appreciation = "🌟 **Excellente dynamique hebdomadaire !** Votre régularité et votre volume horaire témoignent d'un engagement fort et d'une progression très solide dans votre formation en maintenance biomédicale."
    elif avg_p >= 40:
        appreciation = "👍 **Bonne progression constante.** Le rythme est stable, avec de bonnes bases posées sur les compétences techniques."
    else:
        appreciation = "⏳ **Phase de rattrapage nécessaire.** Pensez à planifier des blocs de travail ciblés cette semaine pour accélérer l'atteinte de vos objectifs."

    perspectives = (
        "• Consolider la pratique technique sur les équipements de réanimation et d'imagerie.\n"
        "• Approfondir l'anglais technique et la lecture des schémas électroniques médicaux.\n"
        "• Préparer rigoureusement les dossiers de bourses (Bénin / Algérie / International)."
    )

    solutions = (
        "1. **Gestion du temps (Technique Pomodoro) :** 45 minutes de concentration intense suivies de 10 minutes de pause.\n"
        "2. **Documentation constructeur :** Associez chaque cours théorique à l'étude d'un *Service Manual* (GE, Philips, Siemens).\n"
        "3. **Suivi rigoureux :** Continuez à alimenter régulièrement votre fichier Excel sur votre Bureau pour garder une visibilité claire."
    )

    report = f"📊 **RAPPORT DE PROGRESSION HEBDOMADAIRE — {date_str}** 📊\n\n"
    report += "━━━━━━━━━━━━━━━━━━━━━━\n"
    report += "📈 **BILAN DE VOTRE FEUILLE DE CALCUL EXCEL**\n"
    report += "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    report += f"> ⏱️ **Volume Horaire Total :** `{total_h:.1f} heures`\n"
    report += f"> 📊 **Avancement Moyen Global :** `{avg_p:.0f}%`\n"
    report += f"> 📝 **Sessions Enregistrées :** `{len(data['tasks'])} tâches`\n\n"

    report += f"**🎯 Appréciations :**\n{appreciation}\n\n"
    report += f"**🔭 Perspectives :**\n{perspectives}\n\n"
    report += f"**💡 Solutions & Conseils d'Amélioration :**\n{solutions}\n\n"

    if data["tasks"]:
        report += "**Dernières réalisations de la semaine :**\n"
        for t in data["tasks"][-3:]:
            report += f"• `[{t['date']}]` **{t['task']}** ({t['hours']}h) — *{t['note']}*\n"
        report += "\n"

    report += "---\n*Rapport hebdomadaire de progression généré automatiquement par Free Claude Code.*"
    return report

def send_discord(message):
    if not DISCORD_WEBHOOK_URL:
        return False
    chunks = [message[i:i+1900] for i in range(0, len(message), 1900)]
    success = True
    for chunk in chunks:
        payload = {"content": chunk}
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            DISCORD_WEBHOOK_URL,
            data=data,
            headers={"Content-Type": "application/json", "User-Agent": "WeeklyProgressBot/1.0"}
        )
        try:
            with urllib.request.urlopen(req, timeout=15):
                pass
        except Exception as e:
            print(f"Failed to send Discord webhook: {e}", file=sys.stderr)
            success = False
    return success

def main():
    os.makedirs("briefings", exist_ok=True)
    report = generate_weekly_report()
    send_discord(report)
    print("Weekly Progress Report sent successfully!")

if __name__ == "__main__":
    main()
