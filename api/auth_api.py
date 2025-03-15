from fastapi import APIRouter, HTTPException, Response, Form, Depends
from services.companies_service import get_companies, get_company_by_user
from services.auth_service import signin, logout
from middleware.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
async def login(response: Response, email: str = Form(...), password: str = Form(...)):
    return signin(email, password, response)


@router.post("/logout")
async def logout_session(response: Response, current_user: dict = Depends(get_current_user)):
    try:
        return logout(response)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
