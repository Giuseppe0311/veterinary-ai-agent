from clients.supabase_client import get_supabase_client_instance
from fastapi import HTTPException, UploadFile, Response
import os
import uuid

from services.companies_service import get_company_by_user

supabase_client = get_supabase_client_instance()


async def upload_company_documents(file: UploadFile, custom_filename: str, current_user: str):
    storage_path = None
    try:
        # Validate number of documents
        company_documents = get_company_documents_by_user_id(current_user)
        if len(company_documents) >= 3:
            raise HTTPException(status_code=400, detail="Solo se permiten 3 documentos por empresa")

        # Validate file extension
        file_extension = os.path.splitext(file.filename)[1]
        if file_extension not in [".pdf", ".txt"]:
            raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF o TXT")
        file_content = await file.read()
        document_size = len(file_content) / (1024 * 1024)

        document_total_size = sum([float(doc["document_size"]) for doc in company_documents])
        if (document_total_size + document_size) > 3:
            raise HTTPException(status_code=400, detail="El tamaño total de los documentos no puede superar los 3MB")

        # Get company information
        company_information = get_company_by_user(current_user)

        # Generate unique name and prepare for storage
        unique_storage_name = f"{uuid.uuid4()}{file_extension}"
        storage_path = f"{current_user}/{unique_storage_name}"

        # Upload to storage
        storage_response = (
            supabase_client
            .storage
            .from_("company_docs")
            .upload(
                path=storage_path,
                file=file_content,
                file_options={"content-type": file.content_type}
            )
        )

        # Prepare document data
        document_data = {
            "company_phone_number": company_information["phone_number"],
            "document_name": custom_filename,
            "document_type": file_extension,
            "document_size": document_size,
            "document_path": storage_path,
            "original_filename": file.filename,
            "user_id": current_user
        }

        # Save to database
        db_response = supabase_client.table("documents").insert(document_data).execute()

        if db_response.data:
            return db_response.data[0]
        else:
            # Clean up storage if database insertion fails
            supabase_client.storage.from_("company_docs").remove([storage_path])
            raise HTTPException(status_code=500, detail="Error guardando metadata")

    except HTTPException as he:
        if storage_path:
            try:
                supabase_client.storage.from_("company_docs").remove([storage_path])
            except Exception:
                pass
        raise he
    except Exception as e:
        if storage_path:
            try:
                supabase_client.storage.from_("company_docs").remove([storage_path])
            except Exception:
                pass
        raise HTTPException(status_code=500, detail=f"Error al subir documento: {str(e)}")


def get_company_documents_by_id(user_id, document_id):
    response = (supabase_client
                .table("documents")
                .select("*")
                .eq("document_id", document_id)
                .eq("user_id", user_id)
                # .eq("document_status", True)
                .execute())

    if response.data:
        return response.data[0]
    else:
        raise HTTPException(status_code=404, detail="Documento no encontrado o no pertenece al usuario")


def get_company_documents_by_user_id(user_id: str):
    company_response = (supabase_client
                        .table("companies")
                        .select("*")
                        .eq('user_id', user_id)
                        .execute())
    if not company_response.data:
        raise HTTPException(status_code=404, detail="User not found in Company")

    documents_response = (supabase_client
                          .table("documents")
                          .select("*")
                          .eq('user_id', user_id)
                          .eq("document_status", True)
                          .execute())
    if documents_response.data:
        return documents_response.data
    else:
        return []


def get_signed_document_url(document_id, current_user):
    document = get_company_documents_by_id(current_user, document_id)
    signed_response = supabase_client.storage.from_("company_docs").create_signed_url(document["document_path"], 60)
    if not signed_response:
        raise HTTPException(status_code=500, detail="Error generando URL firmada")

    return {"signed_url": signed_response["signedURL"]}


def delete_company_document(document_id, current_user):
    document = get_company_documents_by_id(current_user, document_id)
    response = (supabase_client.table("documents")
                .update({"document_status": False})
                .eq("document_id", document_id)
                .execute())

    if not response:
        raise HTTPException(status_code=500, detail="Error eliminando documento")

    storage_response = supabase_client.storage.from_("company_docs").remove([document["document_path"]])

    print(storage_response, "storage_response")

    if not storage_response:
        raise HTTPException(status_code=500, detail="Error eliminando documento de almacenamiento")

    return Response(status_code=204)
