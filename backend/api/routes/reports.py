import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from api.dependencies.db import get_db
from api.dependencies.tenant import get_tenant_id
from services.report_service import ReportService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/cbam/{year}")
async def get_cbam_annual_report(
    year: int,
    producer_id: str = Query(None),
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
):
    service = ReportService(db)
    report = await service.generate_cbam_report(year, producer_id)
    if not report:
        raise HTTPException(404, "No data for the requested year")
    return report


@router.get("/cbam/{year}/download")
async def download_cbam_report(
    year: int,
    format: str = "json",  # json, csv, pdf
    producer_id: str = Query(None),
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
):
    service = ReportService(db)
    if format == "json":
        report = await service.generate_cbam_report(year, producer_id)
        return report
    elif format == "csv":
        csv_data = await service.export_csv(year)
        return Response(content=csv_data, media_type="text/csv")
    elif format == "pdf":
        pdf_bytes = await service.export_pdf(year, producer_id)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="CBAM_Report_{year}.pdf"'}
        )
    else:
        raise HTTPException(400, "Unsupported format")

