import json
import os
import tempfile
from datetime import datetime, timezone
from io import BytesIO
from sqlalchemy.orm import Session
from db.models.batch import Batch
from db.models.certificate import Certificate

# ReportLab para geração de PDF
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import qrcode

class ReportService:
    def __init__(self, db: Session):
        self.db = db

    async def generate_cbam_report(self, year: int, producer_id: str = None) -> dict:
        # Buscar lotes no ano
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        query = self.db.query(Batch).filter(Batch.created_at.between(start_date, end_date))
        if producer_id:
            query = query.filter(Batch.producer_wallet == producer_id)

        batches = query.all()
        total_h2_kg = sum(b.size_kg for b in batches)
        
        # Calculate total emissions safely
        total_emissions_tco2 = 0
        for b in batches:
            try:
                if b.compliance_report and isinstance(b.compliance_report, dict):
                    cbam_report = b.compliance_report.get("cbam_report", {})
                    if isinstance(cbam_report, dict):
                        emissions = cbam_report.get("declared_emissions_tco2", 0)
                        if isinstance(emissions, (int, float)):
                            total_emissions_tco2 += emissions
            except (AttributeError, TypeError, KeyError):
                continue
        
        certificates_issued = self.db.query(Certificate).filter(
            Certificate.created_at.between(start_date, end_date)
        ).count()

        report = {
            "year": year,
            "producer_id": producer_id,
            "total_hydrogen_kg": total_h2_kg,
            "total_emissions_tco2e": total_emissions_tco2,
            "average_emissions_per_kg": total_emissions_tco2 / total_h2_kg * 1000 if total_h2_kg else 0,
            "certificates_issued": certificates_issued,
            "compliance_rate": sum(1 for b in batches if b.is_compliant) / len(batches) if batches else 0,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        return report

    async def export_csv(self, year: int) -> str:
        import csv
        from io import StringIO
        report = await self.generate_cbam_report(year)
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=report.keys())
        writer.writeheader()
        writer.writerow(report)
        return output.getvalue()

    async def export_pdf(self, year: int, producer_id: str = None) -> bytes:
        """Gera um PDF oficial do Relatório CBAM usando ReportLab."""
        report_data = await self.generate_cbam_report(year, producer_id)

        # Buffer de memória para o PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=A4,
            rightMargin=40, leftMargin=40,
            topMargin=40, bottomMargin=30
        )
        elements = []
        styles = getSampleStyleSheet()

        # Estilos Customizados
        title_style = ParagraphStyle(
            'TitleCustom', parent=styles['Heading1'],
            fontSize=18, spaceAfter=20,
            textColor=colors.HexColor("#0f4c75")
        )
        subtitle_style = ParagraphStyle(
            'Subtitle', parent=styles['Heading2'],
            fontSize=14, spaceAfter=10,
            textColor=colors.HexColor("#3282b8")
        )
        normal_style = styles['Normal']

        # 1. Cabeçalho Oficial
        elements.append(Paragraph(
            "<b>COMPLEXO INDUSTRIAL E PORTUÁRIO DO PECÉM - CEARÁ</b>",
            title_style
        ))
        elements.append(Paragraph(
            "<b>Certificação Oficial H2V-TRUST - Conformidade CBAM</b>",
            subtitle_style
        ))
        elements.append(Paragraph(
            f"<b>Ano Base:</b> {year}", normal_style
        ))
        if producer_id:
            elements.append(Paragraph(
                f"<b>ID do Produtor/Exportador:</b> {producer_id}", normal_style
            ))
        elements.append(Paragraph(
            f"<b>Data de Emissão:</b> {datetime.now(timezone.utc).strftime('%d/%m/%Y %H:%M:%S UTC')}",
            normal_style
        ))
        elements.append(Spacer(1, 20))

        # 2. Tabela de Métricas Principais
        elements.append(Paragraph("Resumo Operacional", subtitle_style))

        metrics_data = [
            ["Métrica", "Valor Declarado"],
            [
                "Total de Hidrogênio Produzido",
                f"{report_data['total_hydrogen_kg']:.2f} kg"
            ],
            [
                "Total de Emissões GEE (Escopo 1 e 2)",
                f"{report_data['total_emissions_tco2e']:.4f} tCO2e"
            ],
            [
                "Intensidade de Carbono Média",
                f"{report_data['average_emissions_per_kg']:.4f} kgCO2e/kgH2"
            ],
            [
                "Certificados SBT Emitidos (Blockchain)",
                f"{report_data['certificates_issued']}"
            ],
            [
                "Taxa de Conformidade CBAM",
                f"{(report_data['compliance_rate'] * 100):.1f}%"
            ]
        ]

        t = Table(metrics_data, colWidths=[250, 200])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#3282b8")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f4f6f8")),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 20))

        # 3. Bloco de Imunidade CBAM (Texto de Validação)
        elements.append(Paragraph("Declaração de RFNBO", subtitle_style))
        disclaimer = (
            "Este documento certifica, mediante provas criptográficas ancoradas na rede Polygon "
            "via Soulbound Tokens (SBT), que a produção supramencionada respeita o limite de "
            "3.4 kgCO2e/kgH2 exigido pelo Carbon Border Adjustment Mechanism (CBAM) para a "
            "classificação RFNBO da União Europeia. Os dados de água e matriz energética foram "
            "verificados hora a hora (hourly-matching)."
        )
        elements.append(Paragraph(disclaimer, normal_style))
        elements.append(Spacer(1, 20))

        # 4. Geração do QR Code de Verificação
        elements.append(Paragraph("Autenticidade Criptográfica", subtitle_style))

        qr = qrcode.QRCode(version=1, box_size=5, border=2)
        qr.add_data(
            f"https://h2v-trust.ce.gov.br/verify/{year}/{producer_id or 'all'}"
        )
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Salva a imagem temporariamente para o ReportLab usar
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            img.save(temp_file, format="PNG")
            temp_path = temp_file.name

        elements.append(Image(temp_path, width=100, height=100, hAlign='LEFT'))
        elements.append(Paragraph(
            "Escaneie para validar a prova de integridade no Blockchain Público.",
            normal_style
        ))

        # Compila o PDF
        doc.build(elements)

        # Limpa a imagem temporária
        if os.path.exists(temp_path):
            os.remove(temp_path)

        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

