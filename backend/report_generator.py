
from io import BytesIO
from datetime import datetime, timezone

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_production_report(plan):
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph("SMARTROLL", styles["Title"])
    )

    elements.append(
        Paragraph(
            "Production Planning Engineering Report",
            styles["Heading2"],
        )
    )

    generated_at = datetime.now(
        timezone.utc
    ).strftime("%Y-%m-%d %H:%M UTC")

    elements.append(
        Paragraph(
            f"Generated: {generated_at}",
            styles["Normal"],
        )
    )

    elements.append(Spacer(1, 20))

    rows = [
        ["Production Metric", "Estimated Value"],
        ["Quantity", f"{plan['quantity']:,} parts"],
        [
            "Total Material Length",
            f"{plan['total_length_m']:,.2f} m",
        ],
        [
            "Net Material Weight",
            f"{plan['net_weight_kg']:,.2f} kg",
        ],
        [
            "Gross Material Weight",
            f"{plan['gross_weight_kg']:,.2f} kg",
        ],
        [
            "Estimated Waste",
            f"{plan['estimated_waste_kg']:,.2f} kg",
        ],
        [
            "Material Cost (CAD)",
            f"${plan['material_cost']:,.2f}",
        ],
        [
            "Production Run Time",
            f"{plan['run_time_min']:,.2f} min",
        ],
        [
            "Machine Setup Time",
            f"{plan['setup_time_min']:,.2f} min",
        ],
        [
            "Total Production Time",
            f"{plan['total_time_min']:,.2f} min",
        ],
        [
            "Estimated 8-Hour Shifts",
            str(plan["estimated_shifts_8h"]),
        ],
    ]

    table = Table(
        rows,
        colWidths=[260, 230],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#17324D"),
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white,
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold",
            ),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [
                    colors.white,
                    colors.HexColor("#F0F4F8"),
                ],
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.3,
                colors.lightgrey,
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE",
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                9,
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                9,
            ),
        ])
    )

    elements.append(table)
    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "Engineering Assumptions",
            styles["Heading2"],
        )
    )

    for assumption in plan["assumptions"]:
        elements.append(
            Paragraph(
                f"&#8226; {assumption}",
                styles["Normal"],
            )
        )
        elements.append(Spacer(1, 5))

    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph(
            "DISCLAIMER: This document contains "
            "preliminary planning estimates based on "
            "demonstration inputs. It is not a certified "
            "engineering or manufacturing approval.",
            styles["Normal"],
        )
    )

    document.build(elements)

    buffer.seek(0)
    return buffer.getvalue()
