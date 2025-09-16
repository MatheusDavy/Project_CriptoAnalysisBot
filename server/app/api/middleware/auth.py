from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.utils.jwt import verify_jwt

async def auth_middleware(request: Request):
	token = request.cookies.get("access_token")

	if not token:
		raise HTTPException(
			status_code=401,
			detail="Invalid Token"
		)

	try:
		verify_jwt(token)
	except Exception:
		raise HTTPException(
			status_code=401,
			detail="Invalid Token"
		)