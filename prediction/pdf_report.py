from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.units import inch


def generate_prediction_report(
    response,
    username,
    month,
    prediction,
    estimated_bill,
    consumption_level,
    top_energy_factors,
    recommendations,
):
    """
    Generate a downloadable PDF prediction report.
    """

    pdf = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=10,
    )

    normal_style = ParagraphStyle(
        "ReportNormal",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
    )

    story = []

    # Title
    story.append(
        Paragraph(
            "Smart Household Electricity<br/>"
            "Consumption & Bill Prediction Report",
            title_style,
        )
    )

    story.append(Spacer(1, 10))

    # User information
    story.append(
        Paragraph("Prediction Details", heading_style)
    )

    details = [
        ["Username", str(username)],
        ["Month", str(month)],
        [
            "Predicted Consumption",
            f"{float(prediction):.2f} kWh",
        ],
        [
            "Estimated Monthly Bill",
            f"₹{float(estimated_bill):.2f}",
        ],
        ["Consumption Level", str(consumption_level)],
    ]

    details_table = Table(
        details,
        colWidths=[2.3 * inch, 3.5 * inch],
    )

    details_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ])
    )

    story.append(details_table)

    # Top energy factors
    story.append(
        Paragraph(
            "Top Energy-Consuming Factors",
            heading_style,
        )
    )

    if top_energy_factors:

        factor_data = [
            ["Rank", "Factor", "Description", "Impact"]
        ]

        for index, factor in enumerate(
            top_energy_factors,
            start=1
        ):
            factor_data.append([
                str(index),
                str(factor.get("name", "")),
                str(factor.get("description", "")),
                str(factor.get("impact", "")),
            ])

        factor_table = Table(
            factor_data,
            colWidths=[
                0.5 * inch,
                1.5 * inch,
                2.6 * inch,
                1.0 * inch,
            ],
        )

        factor_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ])
        )

        story.append(factor_table)

    else:
        story.append(
            Paragraph(
                "No energy-consuming factors available.",
                normal_style,
            )
        )

    # Recommendations
    story.append(
        Paragraph(
            "Personalized Energy-Saving Recommendations",
            heading_style,
        )
    )

    if recommendations:

        for index, recommendation in enumerate(
            recommendations,
            start=1
        ):
            if isinstance(recommendation, dict):
                text = recommendation.get(
                    "text",
                    str(recommendation)
                )
            else:
                text = str(recommendation)

            story.append(
                Paragraph(
                    f"{index}. {text}",
                    normal_style,
                )
            )

            story.append(Spacer(1, 5))

    else:
        story.append(
            Paragraph(
                "No personalized recommendations available.",
                normal_style,
            )
        )

    # Footer text
    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "This report is generated by the Smart Household "
            "Electricity Consumption & Electricity Bill Prediction System.",
            normal_style,
        )
    )

    pdf.build(story)
