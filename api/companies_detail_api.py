from fastapi import APIRouter, HTTPException
from services.company_details_service import get_company_details, get_company_by_number

router = APIRouter(prefix="/company-details", tags=["Companies Details"])


@router.get("/")
async def api_get_companies_details():
    companies_details = get_company_details()
    return companies_details


@router.get("/{number_id}")
async def api_get_company_by_number(number_id: str):
    single_companies_details = get_company_by_number(number_id)
    if single_companies_details:
        return single_companies_details
    else:
        raise HTTPException(status_code=404, detail="Company not found")
