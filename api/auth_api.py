from fastapi import APIRouter, HTTPException, Response, Form
from services.companies_service import get_companies, get_company_by_user
from services.auth_service import signin

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
async def login(response: Response, email: str = Form(...), password: str = Form(...)):
    try:
        return signin(email, password, response)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
