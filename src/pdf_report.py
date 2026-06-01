from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import json
import os
from datetime import datetime

BG      = colors.HexColor('#05050F')
PURPLE  = colors.HexColor('#9D4EDD')
GOLD    = colors.HexColor('#FFD700')
GREEN   = colors.HexColor('#00FF88')
RED     = colors.HexColor('#FF2255')
YELLOW  = colors.HexColor('#FFD740')
GRAY    = colors.HexColor('#8888AA')
WHITE   = colors.white
DARK    = colors.HexColor('#0D0D1F')

def generate_report(alerts, blocked_ips, stats, output_path='../logs/cybersentinel_report.pdf'):
    """Generate a professional PDF security report"""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        doc  = SimpleDocTemplate(output_path, pagesize=A4,
                                  rightMargin=40, leftMargin=40,
                                  topMargin=40, bottomMargin=40)
        story = []
        styles = getSampleStyleSheet()

        # ─── Title Style ──────────────────────────────────
        title_style = ParagraphStyle(
            'Title', parent=styles['Title'],
            fontSize=28, textColor=GOLD,
            alignment=TA_CENTER, spaceAfter=6,
            fontName='Helvetica-Bold'
        )
        subtitle_style = ParagraphStyle(
            'Subtitle', parent=styles['Normal'],
            fontSize=12, textColor=GRAY,
            alignment=TA_CENTER, spaceAfter=4
        )
        heading_style = ParagraphStyle(
            'Heading', parent=styles['Normal'],
            fontSize=14, textColor=PURPLE,
            spaceAfter=8, spaceBefore=16,
            fontName='Helvetica-Bold'
        )
        normal_style = ParagraphStyle(
            'Body', parent=styles['Normal'],
            fontSize=10, textColor=WHITE,
            spaceAfter=4
        )

        # ─── Header ───────────────────────────────────────
        story.append(Paragraph("⚔ CyberSentinel", title_style))
        story.append(Paragraph("AI-Powered Intrusion Detection & Prevention System", subtitle_style))
        story.append(Paragraph(f"Security Report — Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", subtitle_style))
        story.append(Spacer(1, 20))

        # ─── Summary Stats Table ──────────────────────────
        story.append(Paragraph("Executive Summary", heading_style))

        total    = stats.get('total', 0)
        attacks  = stats.get('attacks', 0)
        normal   = stats.get('normal', 0)
        severe   = stats.get('severe', 0)
        moderate = stats.get('moderate', 0)
        suspicious = stats.get('suspicious', 0)
        blocked  = stats.get('auto_blocked', 0)

        summary_data = [
            ['Metric', 'Value', 'Status'],
            ['Total Traffic Analyzed', str(total), 'Monitored'],
            ['Normal Traffic', str(normal), 'Safe'],
            ['Attacks Detected', str(attacks), 'Threat'],
            ['Severe Threats', str(severe), 'Critical'],
            ['Moderate Threats', str(moderate), 'Warning'],
            ['Suspicious Traffic', str(suspicious), 'Monitor'],
            ['Auto-Blocked IPs', str(blocked), 'Protected'],
            ['Blocked IP Count', str(stats.get('blocked_ips', 0)), 'Blocked'],
            ['Model Accuracy', '99.92%', 'Excellent'],
        ]

        summary_table = Table(summary_data, colWidths=[250, 120, 120])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND',  (0, 0), (-1, 0),  PURPLE),
            ('TEXTCOLOR',   (0, 0), (-1, 0),  WHITE),
            ('FONTNAME',    (0, 0), (-1, 0),  'Helvetica-Bold'),
            ('FONTSIZE',    (0, 0), (-1, 0),  11),
            ('ALIGN',       (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND',  (0, 1), (-1, -1), DARK),
            ('TEXTCOLOR',   (0, 1), (-1, -1), WHITE),
            ('FONTSIZE',    (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [DARK, BG]),
            ('GRID',        (0, 0), (-1, -1), 0.5, PURPLE),
            ('TOPPADDING',  (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING',(0, 0), (-1, -1), 8),
            # Color code status column
            ('TEXTCOLOR',   (2, 2), (2, 2),  GREEN),   # Safe
            ('TEXTCOLOR',   (2, 3), (2, 3),  RED),     # Threat
            ('TEXTCOLOR',   (2, 4), (2, 4),  RED),     # Critical
            ('TEXTCOLOR',   (2, 5), (2, 5),  YELLOW),  # Warning
            ('TEXTCOLOR',   (2, 6), (2, 6),  GRAY),    # Monitor
            ('TEXTCOLOR',   (2, 7), (2, 7),  GREEN),   # Protected
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))

        # ─── Recent Alerts Table ──────────────────────────
        story.append(Paragraph("Recent Security Alerts", heading_style))

        alert_data = [['Time', 'Category', 'Confidence', 'Protocol', 'Source IP', 'Description']]

        recent_alerts = alerts[-20:] if len(alerts) > 20 else alerts
        for a in reversed(recent_alerts):
            alert_data.append([
                str(a.get('time', '—')),
                str(a.get('category', '—')),
                str(a.get('confidence', '—')) + '%',
                str(a.get('protocol', '—')),
                str(a.get('src_ip', '—')),
                str(a.get('description', '—'))[:40]
            ])

        if len(alert_data) == 1:
            alert_data.append(['No alerts recorded', '—', '—', '—', '—', '—'])

        alert_table = Table(alert_data, colWidths=[65, 100, 70, 55, 95, 105])
        alert_style = [
            ('BACKGROUND',  (0, 0), (-1, 0),  PURPLE),
            ('TEXTCOLOR',   (0, 0), (-1, 0),  WHITE),
            ('FONTNAME',    (0, 0), (-1, 0),  'Helvetica-Bold'),
            ('FONTSIZE',    (0, 0), (-1, 0),  9),
            ('ALIGN',       (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND',  (0, 1), (-1, -1), DARK),
            ('TEXTCOLOR',   (0, 1), (-1, -1), WHITE),
            ('FONTSIZE',    (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [DARK, BG]),
            ('GRID',        (0, 0), (-1, -1), 0.5, PURPLE),
            ('TOPPADDING',  (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING',(0, 0), (-1, -1), 6),
        ]

        # Color code category rows
        for i, a in enumerate(recent_alerts, 1):
            cat = a.get('category', '')
            if cat == 'SEVERE THREAT':
                alert_style.append(('TEXTCOLOR', (1, i), (1, i), RED))
            elif cat == 'MODERATE THREAT':
                alert_style.append(('TEXTCOLOR', (1, i), (1, i), YELLOW))
            elif cat == 'SUSPICIOUS':
                alert_style.append(('TEXTCOLOR', (1, i), (1, i), GRAY))
            else:
                alert_style.append(('TEXTCOLOR', (1, i), (1, i), GREEN))

        alert_table.setStyle(TableStyle(alert_style))
        story.append(alert_table)
        story.append(Spacer(1, 20))

        # ─── Blocked IPs Table ────────────────────────────
        if blocked_ips:
            story.append(Paragraph("Blocked IP Addresses", heading_style))
            blocked_data = [['IP Address', 'Time Blocked', 'Reason', 'Confidence']]
            for ip, info in blocked_ips.items():
                blocked_data.append([
                    str(ip),
                    str(info.get('time', '—')),
                    str(info.get('reason', '—')),
                    str(info.get('confidence', '—')) + '%'
                ])

            blocked_table = Table(blocked_data, colWidths=[130, 100, 170, 90])
            blocked_table.setStyle(TableStyle([
                ('BACKGROUND',  (0, 0), (-1, 0),  RED),
                ('TEXTCOLOR',   (0, 0), (-1, 0),  WHITE),
                ('FONTNAME',    (0, 0), (-1, 0),  'Helvetica-Bold'),
                ('FONTSIZE',    (0, 0), (-1, 0),  10),
                ('ALIGN',       (0, 0), (-1, -1), 'CENTER'),
                ('BACKGROUND',  (0, 1), (-1, -1), DARK),
                ('TEXTCOLOR',   (0, 1), (-1, -1), RED),
                ('FONTSIZE',    (0, 1), (-1, -1), 9),
                ('GRID',        (0, 0), (-1, -1), 0.5, RED),
                ('TOPPADDING',  (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING',(0, 0), (-1, -1), 6),
            ]))
            story.append(blocked_table)
            story.append(Spacer(1, 20))

        # ─── Footer ───────────────────────────────────────
        story.append(Spacer(1, 20))
        story.append(Paragraph(
            "CyberSentinel AI-IDS/IPS — Confidential Security Report",
            subtitle_style
        ))
        story.append(Paragraph(
            f"Generated by CyberSentinel v1.0 | {datetime.now().strftime('%Y-%m-%d')}",
            subtitle_style
        ))

        doc.build(story)
        print(f"PDF report generated: {output_path}")
        return True, output_path

    except Exception as e:
        print(f"PDF generation error: {e}")
        return False, str(e)