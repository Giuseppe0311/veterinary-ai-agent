from clients.supabase_client import get_supabase_client_instance
from fastapi import HTTPException, Response

supabase_client = get_supabase_client_instance()


def signin(email: str, password: str, response: Response):
    response_data = supabase_client.auth.sign_in_with_password({
        'email': email,
        'password': password
    })

    if response_data.user is None:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = response_data.session.access_token
    # refresh_token = response_data.session.refresh_token
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True
    )

    return {"status": "success", "message": "Login exitoso"}
