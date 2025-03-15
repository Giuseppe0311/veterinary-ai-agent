from gotrue.errors import AuthApiError

from clients.supabase_client import get_supabase_client_instance
from fastapi import HTTPException, Response

supabase_client = get_supabase_client_instance()


def signin(email: str, password: str, response: Response):
    try:
        response_data = supabase_client.auth.sign_in_with_password({
            'email': email,
            'password': password
        })
    except AuthApiError as e:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en el servidor")

    access_token = response_data.session.access_token
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="Lax"
    )
    return {"status": "success", "message": "Login exitoso"}


def logout(response: Response):
    supabase_client.auth.sign_out()
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="Lax"
    )
    return {"status": "success", "message": "Logout exitoso"}
