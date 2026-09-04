import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, PieChart, Reference
import os
import shutil

def create_tracker():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Suivi & Bilan Hebdomadaire"

    # Ensure grid lines are visible
    ws.views.sheetView[0].showGridLines = True

    # Color Palette (Professional Navy & Slate)
    NAVY_HEADER = "1E3A8A"      # Dark Blue for headers
    HEADER_TEXT = "FFFFFF"      # White text
    ZEBRA_FILL = "F8FAFC"       # Light off-white for alternating rows
    ACCENT_BLUE = "2563EB"      # Accent blue
    BORDER_COLOR = "CBD5E1"     # Slate 300
    GRAY_TEXT = "64748B"        # Slate 500

    # Fonts & Fills
    font_title = Font(name="Segoe UI", size=18, bold=True, color="1E293B")
    font_subtitle = Font(name="Segoe UI", size=11, italic=True, color=GRAY_TEXT)
    font_section = Font(name="Segoe UI", size=13, bold=True, color="1E3A8A")
    font_header = Font(name="Segoe UI", size=11, bold=True, color=HEADER_TEXT)
    font_data = Font(name="Segoe UI", size=11, color="0F172A")
    font_bold = Font(name="Segoe UI", size=11, bold=True, color="0F172A")

    fill_header = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
    fill_zebra = PatternFill(start_color=ZEBRA_FILL, end_color=ZEBRA_FILL, fill_type="solid")
    fill_summary = PatternFill(start_color="EFF6FF", end_color="EFF6FF", fill_type="solid")

    thin_border = Border(
        left=Side(style='thin', color=BORDER_COLOR),
        right=Side(style='thin', color=BORDER_COLOR),
        top=Side(style='thin', color=BORDER_COLOR),
        bottom=Side(style='thin', color=BORDER_COLOR)
    )

    thick_bottom = Border(
        left=Side(style='thin', color=BORDER_COLOR),
        right=Side(style='thin', color=BORDER_COLOR),
        top=Side(style='thin', color=BORDER_COLOR),
        bottom=Side(style='medium', color="1E3A8A")
    )

    # Title Block
    ws['A1'] = "Tableau de Bord - Objectifs Prioritaires, Suivi & Bilan"
    ws['A1'].font = font_title
    ws['A2'] = "Suivi stratégique par ordre de priorité, avancement quotidien, temps de travail et bilans hebdomadaires"
    ws['A2'].font = font_subtitle

    # KPI / Summary Cards (Rows 4-5)
    ws['A4'] = "Total Heures"
    ws['B4'] = "=SUM(C18:C34)"
    ws['D4'] = "Progression Moyenne"
    ws['E4'] = "=AVERAGE(D18:D34)"

    for col in ['A', 'B', 'D', 'E']:
        cell = ws[f'{col}4']
        cell.font = font_bold
        cell.fill = fill_summary
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

        val_cell = ws[f'{col}5']
        val_cell.font = font_title
        val_cell.fill = fill_summary
        val_cell.alignment = Alignment(horizontal="center", vertical="center")
        val_cell.border = thin_border

    ws['A5'] = "=B4"
    ws['B5'].number_format = '0.0 "h"'
    ws['D5'] = "=E4"
    ws['E5'].number_format = '0%'

    # ==================== TABLE 0: OBJECTIFS FIXÉS PAR PRIORITÉ (Rows 7-14) ====================
    ws['A7'] = "0. Objectifs Fixés pour la Semaine (Classés par Ordre de Priorité)"
    ws['A7'].font = font_section

    goal_headers = ["Priorité", "Objectif / Tâche Fixée", "Niveau d'Importance", "Poids (%)", "Statut Actuel"]
    for col_idx, header in enumerate(goal_headers, start=1):
        cell = ws.cell(row=8, column=col_idx, value=header)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thick_bottom

    goals_data = [
        (1, "Résolution des problèmes de CI/CD et tests robustes", "Critique", 0.40, "Atteint 🎯"),
        (2, "Migration modulaire de l'architecture & core/", "Important", 0.30, "En cours ⏳"),
        (3, "Documentation technique & guides d'utilisation", "Moyen", 0.20, "En cours ⏳"),
        (4, "Optimisations mineures et nettoyage du code", "Faible", 0.10, "À planifier ⏸️"),
    ]

    for row_idx, row_data in enumerate(goals_data, start=9):
        for col_idx, val in enumerate(row_data, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.font = font_data
            cell.border = thin_border
            if row_idx % 2 == 0:
                cell.fill = fill_zebra

            if col_idx == 1:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx == 2:
                cell.alignment = Alignment(horizontal="left", vertical="center")
            elif col_idx == 3:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx == 4:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                cell.number_format = '0%'
            elif col_idx == 5:
                cell.alignment = Alignment(horizontal="center", vertical="center")

    # ==================== TABLE 1: SUIVI QUOTIDIEN (Rows 16-34) ====================
    ws['A16'] = "1. Suivi Quotidien de l'Avancement"
    ws['A16'].font = font_section

    headers = ["Date", "Tâches Réalisées", "Temps Passé (h)", "Progression (%)", "Notes / Bloquants", "Appréciation / Statut"]
    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=17, column=col_idx, value=header)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thick_bottom

    sample_data = [
        # Semaine 31 (Rows 18-24)
        ("2026-08-01", "Cadrage du projet et spécifications techniques", 6.5, 0.20, "Validation OK"),
        ("2026-08-02", "Mise en place de l'architecture de base", 7.0, 0.35, "Dépendances résolues"),
        ("2026-08-03", "Développement du module principal et tests unitaires", 8.0, 0.50, "RAS"),
        ("2026-08-04", "Intégration des APIs et gestion des erreurs", 7.5, 0.65, "Légère latence API testée"),
        ("2026-08-05", "Optimisation des performances et revue de code", 6.0, 0.75, "Ruff & ty validés"),
        ("2026-08-06", "Rédaction de la documentation technique", 5.0, 0.85, "En cours"),
        ("2026-08-07", "Tests de charge et validation finale", 7.0, 1.00, "Objectif atteint avec succès !"),
        # Semaine 32 (Rows 25-27)
        ("2026-08-11", "Audit de sécurité et revue des dépendances", 6.0, 0.20, "Sécurité validée"),
        ("2026-08-12", "Refactorisation des utilitaires partagés", 7.0, 0.55, "Structure modulaire améliorée"),
        ("2026-08-13", "Mise en place des règles de CI/CD et tests robustes", 8.0, 1.00, "Pipeline opérationnel"),
        # Semaine 33 (Rows 28-31)
        ("2026-08-18", "Migration de l'architecture vers une structure modulaire", 7.5, 0.30, "Conflits de dépendances / imports circulaires"),
        ("2026-08-19", "Résolution des cycles d'import et protocoles partagés", 8.0, 0.60, "Code épuré et validé par Ruff/ty"),
        ("2026-08-20", "Développement des scripts d'automatisation CI/CD & tests", 7.0, 0.85, "Temps de build un peu long sur le pipeline"),
        ("2026-08-21", "Revue de code finale, documentation & déploiement test", 6.5, 1.00, "Tout est validé avec succès !"),
    ]

    for row_idx, row_data in enumerate(sample_data, start=18):
        for col_idx, val in enumerate(row_data, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.font = font_data
            cell.border = thin_border

            if row_idx % 2 == 0:
                cell.fill = fill_zebra

            if col_idx == 1:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx == 2:
                cell.alignment = Alignment(horizontal="left", vertical="center")
            elif col_idx == 3:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                cell.number_format = '0.0'
            elif col_idx == 4:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                cell.number_format = '0%'
            elif col_idx == 5:
                cell.alignment = Alignment(horizontal="left", vertical="center")

        appr_cell = ws.cell(row=row_idx, column=6)
        appr_cell.value = f'=IF(D{row_idx}>=1, "Objectif Atteint 🎯", IF(D{row_idx}>=0.5, "Bonne Progression 👍", IF(D{row_idx}>0, "En Cours ⏳", "À Planifier ⏸️")))'
        appr_cell.font = font_data
        appr_cell.border = thin_border
        appr_cell.alignment = Alignment(horizontal="center", vertical="center")
        if row_idx % 2 == 0:
            appr_cell.fill = fill_zebra

    # Empty entry rows up to row 34
    for row_idx in range(len(sample_data) + 18, 35):
        for col_idx in range(1, 6):
            cell = ws.cell(row=row_idx, column=col_idx, value="")
            cell.border = thin_border
            if row_idx % 2 == 0:
                cell.fill = fill_zebra
            if col_idx == 3:
                cell.number_format = '0.0'
            elif col_idx == 4:
                cell.number_format = '0%'

        appr_cell = ws.cell(row=row_idx, column=6)
        appr_cell.value = f'=IF(D{row_idx}="","",IF(D{row_idx}>=1, "Objectif Atteint 🎯", IF(D{row_idx}>=0.5, "Bonne Progression 👍", IF(D{row_idx}>0, "En Cours ⏳", "À Planifier ⏸️"))))'
        appr_cell.font = font_data
        appr_cell.border = thin_border
        appr_cell.alignment = Alignment(horizontal="center", vertical="center")
        if row_idx % 2 == 0:
            appr_cell.fill = fill_zebra

    # ==================== TABLE 2: BILAN HEBDOMADAIRE (Rows 37-41) ====================
    start_row_weekly = 37
    ws.cell(row=start_row_weekly, column=1, value="2. Bilan Hebdomadaire & Recommandations Intelligentes (IA)").font = font_section

    weekly_headers = [
        "Semaine",
        "Heures Totales (h)",
        "Avancement Moyen",
        "Réalisations Clés",
        "Objectifs Atteints",
        "Difficultés Rencontrées",
        "Solutions / Nouvelles Approches (IA)"
    ]

    for col_idx, header in enumerate(weekly_headers, start=1):
        cell = ws.cell(row=start_row_weekly + 1, column=col_idx, value=header)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thick_bottom

    weekly_data = [
        ("Semaine 31 (01/08 - 07/08)", "=SUM(C18:C24)", "=AVERAGE(D18:D24)", "Cadrage, architecture initiale, développement module et APIs", "100% des jalons atteints", "Légère latence API constatée", "Mettre en place un cache local et paralléliser les requêtes."),
        ("Semaine 32 (08/08 - 14/08)", "=SUM(C25:C27)", "=AVERAGE(D25:D27)", "Audit de sécurité, refactorisation & pipeline CI/CD", "Validation finale validée", "Volume de tests élevé", "Automatiser les tests de charge dans le pipeline CI/CD."),
        ("Semaine 33 (18/08 - 21/08)", "=SUM(C28:C31)", "=AVERAGE(D28:D31)", "Migration modulaire, résolution des imports & scripts CI/CD", "100% des jalons validés", "Conflits de dépendances & temps de build", "Isoler les types dans core/ et mettre en cache les environnements uv."),
    ]

    for w_idx, w_row in enumerate(weekly_data, start=start_row_weekly + 2):
        for col_idx, val in enumerate(w_row, start=1):
            cell = ws.cell(row=w_idx, column=col_idx, value=val)
            cell.font = font_data
            cell.border = thin_border
            if w_idx % 2 == 0:
                cell.fill = fill_zebra

            if col_idx == 1:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx == 2:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                cell.number_format = '0.0 "h"'
            elif col_idx == 3:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                cell.number_format = '0%'
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

    # Auto-adjust column widths
    col_widths = {
        'A': 28,
        'B': 25,
        'C': 22,
        'D': 45,
        'E': 25,
        'F': 35,
        'G': 48
    }
    for col_letter, width in col_widths.items():
        if col_letter <= 'G':
            ws.column_dimensions[col_letter].width = width

    # ==================== CHARTS (Pie Chart & Line Chart) ====================

    # 1. Pie Chart for Priority Goals Weight (Placed at G7)
    pie = PieChart()
    pie.title = "Répartition des Poids des Objectifs Prioritaires"
    pie.width = 14
    pie.height = 10

    labels_ref = Reference(ws, min_col=2, min_row=9, max_row=12)
    data_ref_pie = Reference(ws, min_col=4, min_row=8, max_row=12)

    pie.add_data(data_ref_pie, titles_from_data=True)
    pie.set_categories(labels_ref)
    ws.add_chart(pie, "G7")

    # 2. Line Chart for Daily Progression over time (Placed at G19)
    chart = LineChart()
    chart.title = "Évolution de la Progression Quotidienne (%)"
    chart.style = 13
    chart.y_axis.title = "Progression"
    chart.y_axis.number_format = '0%'
    chart.x_axis.title = "Date"
    chart.width = 14
    chart.height = 10

    data_ref_line = Reference(ws, min_col=4, min_row=17, max_row=34)
    cats_ref_line = Reference(ws, min_col=1, min_row=18, max_row=34)

    chart.add_data(data_ref_line, titles_from_data=True)
    chart.set_categories(cats_ref_line)

    if chart.series:
        series = chart.series[0]
        series.graphicalProperties.line.solidFill = ACCENT_BLUE
        series.graphicalProperties.line.width = 30000

    ws.add_chart(chart, "G19")

    output_filename = "suivi_progression_travail.xlsx"
    wb.save(output_filename)
    print(f"Local file saved with priority goals table and charts: {output_filename}")

    # Copy to Desktop folder "ma progression"
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    if not os.path.exists(desktop):
        desktop = os.path.join(os.path.expanduser('~'), 'OneDrive', 'Desktop')
    target_dir = os.path.join(desktop, 'ma progression')
    os.makedirs(target_dir, exist_ok=True)
    dst = os.path.join(target_dir, output_filename)
    dst_v2 = os.path.join(target_dir, "Suivi_Travail_Avec_Bilan_Hebdo.xlsx")

    try:
        shutil.copy2(output_filename, dst)
        shutil.copy2(output_filename, dst_v2)
        print(f"Successfully copied updated file to Desktop: {dst_v2}")
    except PermissionError:
        print("Note: Some desktop files are locked by Excel, but local file is fully updated.")

if __name__ == "__main__":
    create_tracker()
