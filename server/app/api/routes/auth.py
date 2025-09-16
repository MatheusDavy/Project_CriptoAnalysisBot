from fastapi import APIRouter, Response, HTTPException, Query
from fastapi.responses import JSONResponse
from app.utils.jwt import create_jwt
from app.env import AUTH_EMAIL, AUTH_PASSWORD, JWT_SUB

router = APIRouter()

@router.get("/login")
async def login(
    response: Response,
    email: str = Query(..., description="Email do usuário"),
    password: str = Query(..., description="Senha do usuário")
):
    if email != AUTH_EMAIL or password != AUTH_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt(JWT_SUB)

    response = JSONResponse(content={"message": "Authenticated"})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=3600,
        samesite="strict",
        secure=False,  # em produção: True
    )

    return response
