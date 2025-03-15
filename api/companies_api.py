from fastapi import APIRouter, HTTPException, Depends

from middleware.auth import get_current_user
from services.companies_service import get_companies, get_company_by_user

router = APIRouter(prefix="/company", tags=["Companies"])


@router.get("/")
async def api_get_companies():
    companies_service = get_companies()
    return companies_service


@router.get("/get-company")
async def api_get_company_by_number(current_user: dict = Depends(get_current_user)):
    companies_service = get_company_by_user(current_user["sub"])
    return companies_service
