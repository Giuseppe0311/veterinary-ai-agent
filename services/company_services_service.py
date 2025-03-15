from clients.supabase_client import get_supabase_client_instance
from fastapi import HTTPException

supabase_client = get_supabase_client_instance()


def get_services():
    response = supabase_client.table("services").select("*").execute()
    if response.data:
        return response.data
    else:
        return []


def get_services_by_number(number_id: str):
    response_single = supabase_client.table("services").select("*").eq('company_phone_number', number_id).execute()
    if response_single.data:
        return response_single.data
    else:
        raise HTTPException(status_code=404, detail="Company Service not found")
