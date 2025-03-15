from clients.supabase_client import get_supabase_client_instance
from fastapi import HTTPException

supabase_client = get_supabase_client_instance()


def get_companies():
    response = supabase_client.table("companies").select("*").execute()
    print(response)
    if response.data:
        return response.data
    else:
        return []


def get_company_by_user(current_user: str):
    response_single = (supabase_client
                       .table("companies")
                       .select("*")
                       .eq('user_id', current_user)
                       .execute())
    if response_single.data:
        return response_single.data[0]
    else:
        raise HTTPException(status_code=404, detail="Company not found")
