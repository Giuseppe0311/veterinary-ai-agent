import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE")


def get_supabase_client_instance() -> Client:
    return create_client(url, key)
