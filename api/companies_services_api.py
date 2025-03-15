from fastapi import APIRouter
from services.company_services_service import get_services, get_services_by_number

router = APIRouter(prefix="/company-services", tags=["Company Services"])


@router.get("/")
async def api_get_services():
    services_service = get_services()
    return services_service


@router.get("/{number_id}")
async def api_get_companies(number_id: str):
    services_service = get_services_by_number(number_id)
    return services_service
