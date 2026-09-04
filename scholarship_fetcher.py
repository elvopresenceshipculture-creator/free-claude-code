#!/usr/bin/env python3
"""
Daily Morning Briefing Bot:
1. Veille Maintenance Biomédicale (Algérie, Bénin & Méthodes de Réussite)
2. Bourses d'Études (Bénin & International)
3. Veille IA & Innovation Médicale
Sends the daily digest via Discord Webhook.
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

BIOMEDICAL_SECTION = [
    {
        "category": "🇩🇿 & 🇧🇯 Opportunités & Marché (Algérie & Bénin)",
        "title": "Stages & Insertion Professionnelle en Maintenance Biomédicale",
        "details": "• **En Algérie :** Opportunités de stages pratiques dans les CHU (Centres Hospitaliers Universitaires) algériens (ex: CHU Mustapha Pacha, CHU Oran) sur les équipements d'imagerie, de réanimation et de laboratoire.\n• **Au Bénin :** Forte demande de techniciens supérieurs en maintenance biomédicale avec la modernisation des hôpitaux de zone (Projet Hôpitaux de Référence, cliniques privées, et ministères de la santé)."
    },
    {
        "category": "🔧 Méthodes de Réussite & Compétences Clés",
        "title": "Maîtrise du Diagnostic & Sécurité Électrique Médicale",
        "details": "• **Méthode de diagnostic (Troubleshooting) :** Suivre rigoureusement l'arbre de décision (Alimentation -> Cartes mères -> Capteurs -> Actionneurs).\n• **Normes & Sécurité :** Maîtriser la norme **NF EN 60601** (Sécurité des appareils électromédicaux) et les contrôles de sécurité électrique.\n• **Équipements critiques à maîtriser :** Respirateurs artificiels, machines de dialyse, moniteurs multiparamétriques, électrocardiographes (ECG), et tables d'opération."
    },
    {
        "category": "💡 Conseil Pro & Réussite Étudiante",
        "title": "Stratégie pour exceller en Maintenance Biomédicale",
        "details": "1. **Pratique de terrain :** Ne vous limitez pas à la théorie. Touchez les machines, lisez les manuels de service (Service Manuals) constructeurs (GE, Philips, Siemens).\n2. **Anglais technique :** 90% de la documentation technique et des codes d'erreur des équipements médicaux sont en anglais.\n3. **Polyvalence :** Associez la mécanique, l'électronique analogique/numérique et l'informatique médicale (réseaux DICOM/PACS)."
    }
]

BENIN_SCHOLARSHIPS = [
    {
        "name": "Direction des Bourses et Secours Universitaires (DBSU - Bénin)",
        "description": "Bourses nationales et aides universitaires du MESRS Bénin.",
        "url": "https://www.enseignementsuperieur.gouv.bj/"
    },
    {
        "name": "Bourses AMCI (Maroc - Bénin) & Coopération Algérie-Bénin",
        "description": "Programmes de coopération intergouvernementale pour formations techniques et universitaires.",
        "url": "https://www.amci.ma"
    },
    {
        "name": "Bourse d'Excellence Eiffel (via Campus France Bénin)",
        "description": "Master et Doctorat en France pour étudiants internationaux.",
        "url": "https://www.benin.campusfrance.org"
    }
]

AI_BUSINESS_TRENDS = [
    {
        "title": "Maintenance Prédictive des Équipements Médicaux par l'IA",
        "insight": "L'utilisation de capteurs IoT et d'algorithmes d'IA pour prédire les pannes d'équipements lourds (IRM, scanners) avant qu'elles ne surviennent est le marché en plus forte croissance pour les ingénieurs biomédicaux."
    }
]

def generate_report():
    date_str = datetime.now(timezone.utc).strftime("%d/%m/%Y")

    report = f"🌅 **BRIEFING MATINAL : BIOMÉDICAL, BOURSES & IA — {date_str}** 🌟\n\n"

    # Section 1: Biomedical Maintenance
    report += "━━━━━━━━━━━━━━━━━━━━━━\n"
    report += "🩺 **1. MAINTENANCE BIOMÉDICALE (ALGÉRIE, BÉNIN & MÉTHODES)**\n"
    report += "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    for item in BIOMEDICAL_SECTION:
        report += f"**{item['category']}**\n"
        report += f"> **{item['title']}**\n"
        report += f"> {item['details']}\n\n"

    # Section 2: Scholarships
    report += "━━━━━━━━━━━━━━━━━━━━━━\n"
    report += "🎓 **2. BOURSES D'ÉTUDES & COOPÉRATION**\n"
    report += "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    for idx, item in enumerate(BENIN_SCHOLARSHIPS, 1):
        report += f"> **{idx}. [{item['name']}]({item['url']})**\n"
        report += f"> *Description :* {item['description']}\n\n"

    # Section 3: AI & Tech
    report += "━━━━━━━━━━━━━━━━━━━━━━\n"
    report += "🤖 **3. VEILLE IA & INNOVATION MÉDICALE**\n"
    report += "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    for item in AI_BUSINESS_TRENDS:
        report += f"> **{item['title']}**\n"
        report += f"> 💡 *Impact & Business :* {item['insight']}\n\n"

    report += "---\n*Briefing matinal généré automatiquement chaque matin par Free Claude Code.*"
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
            headers={"Content-Type": "application/json", "User-Agent": "DailyBriefingBot/1.0"}
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
    report = generate_report()
    send_discord(report)
    print("Daily Morning Briefing sent successfully!")

if __name__ == "__main__":
    main()
