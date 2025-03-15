from fastapi import APIRouter, File, UploadFile, Form, Depends
from middleware.auth import get_current_user
from services.company_documents_service import get_company_documents_by_id, get_company_documents_by_user_id, \
    upload_company_documents, get_signed_document_url,delete_company_document

router = APIRouter(prefix="/company-documents", tags=["Company Documents"], dependencies=[Depends(get_current_user)])


@router.get("/get-own-documents")
async def api_get_company_by_number(current_user: dict = Depends(get_current_user)):
    companies_service = get_company_documents_by_user_id(current_user.get("sub"))
    return companies_service


@router.get("/get-document/{document_id}")
async def api_get_company_documents(current_user: dict = Depends(get_current_user), document_id: str = None):
    companies_service = get_company_documents_by_id(current_user.get("sub"), document_id)
    return companies_service


@router.post("/upload-company-document")
async def api_upload_company_documents(
        file: UploadFile = File(...), filename: str = Form(...), current_user: dict = Depends(get_current_user)
):
    user_id = current_user.get("sub")
    return await upload_company_documents(file, filename, user_id)


@router.get("/file/{document_id}/url")
async def api_get_company_document_url(document_id: str, current_user: dict = Depends(get_current_user)):
    return get_signed_document_url(document_id, current_user.get("sub"))


@router.delete("/delete-document/{document_id}")
async def api_delete_company_document(document_id: str, current_user: dict = Depends(get_current_user)):
    return delete_company_document(document_id, current_user.get("sub"))
