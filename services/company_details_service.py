from clients.supabase_client import get_supabase_client_instance
from fastapi import HTTPException

supabase_client = get_supabase_client_instance()


def get_company_details():
    response = supabase_client.table("company_details").select("*").execute()
    if response.data:
        return response.data
    else:
        return []


def get_company_by_number(number_id: str):
    response_single = supabase_client.table("company_details").select("*").eq('company_phone_number', number_id).execute()
    if response_single.data:
        return response_single.data
    else:
        raise HTTPException(status_code=404, detail="Company Detail not found")
