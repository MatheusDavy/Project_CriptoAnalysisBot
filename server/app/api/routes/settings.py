import ast
from fastapi import Depends, APIRouter, Response, HTTPException, Query
from fastapi import Depends, APIRouter, Response, HTTPException, Query, Path, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, conlist
from typing import List, Literal, Optional
from app.db.supabase import supabase
from app.api.middleware.auth import auth_middleware
from datetime import datetime, timezone

router = router = APIRouter(
  dependencies=[Depends(auth_middleware)]
)

# =======================
# List
@router.get("/list")
async def settings_list():
  response = supabase.table("crypto_settings").select("*").order("created_at", desc=True).execute()
  return getattr(response, "data", [])

# =======================
# Create
class TargetSchema(BaseModel):
    type: Literal["NEXT_CANDLE", "PERCENT"]
    value: int = Field(..., ge=1)
    
class CreateCryptoSettingsSchema(BaseModel):
  name: str = Field(..., min_length=2)
  indicators: List[str] = Field(..., min_items=1)
  candle_patterns: List[str] = Field(..., min_items=1)
  timeranges: List[str] = Field(..., min_items=1)
  timeframes: List[str] = Field(..., min_items=1)
  currencies: List[str] = Field(..., min_items=1)
  min_confluence: int = Field(..., ge=1)
  gain_target: List[TargetSchema] = Field(..., min_items=1)
  loss_target: List[TargetSchema] = Field(..., min_items=1)

@router.post("/create")
async def settings_create(payload: CreateCryptoSettingsSchema = Body(...)):
  try:
    data = payload.dict()
    data['status'] = True
    data['created_at'] = datetime.now(timezone.utc).isoformat()
    
    response = supabase.table("crypto_settings").insert(data).execute()
    return getattr(response, "data", None)
  except Exception as e:
    err_str = e.args[0] if e.args else str(e)
    err_obj = ast.literal_eval(err_str)
    message = err_obj.get("message", str(e))

    raise HTTPException(status_code=400, detail=message)

# =======================
# Get
@router.get("/{id}")
async def settings_get(id: str = Path(...)):
  try:
    response = supabase.table("crypto_settings").select("*").eq("id", id).execute()
    data = getattr(response, "data", None)
    if data and len(data) > 0:
      return data[0]
    return None
  except Exception as e:
    err_str = e.args[0] if e.args else str(e)
    err_obj = ast.literal_eval(err_str)
    message = err_obj.get("message", str(e))

    raise HTTPException(status_code=400, detail=message)

# =======================
# Delete
@router.delete("/delete/{id}")
async def settings_delete(id: str = Path(...)):  
  try:
    response = supabase.table("crypto_settings").delete().eq("id", id).execute()
    return getattr(response, "data", None)
  except Exception as e:
    err_str = e.args[0] if e.args else str(e)
    err_obj = ast.literal_eval(err_str)
    message = err_obj.get("message", str(e))

    raise HTTPException(status_code=400, detail=message)

# =======================
class UpdateCryptoSettingsSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    indicators: Optional[List[str]] = None
    candle_patterns: Optional[List[str]] = None
    timeranges: Optional[List[str]] = None
    timeframes: Optional[List[str]] = None
    currencies: Optional[List[str]] = None
    min_confluence: Optional[int] = Field(None, ge=1)
    gain_target: Optional[List[TargetSchema]] = None
    loss_target: Optional[List[TargetSchema]] = None
    status: Optional[bool] = None
  
# Update
@router.put("/update/{id}")
async def settings_update(id: str = Path(...), payload: UpdateCryptoSettingsSchema = Body(...)):
  try:
    data = {k: v for k, v in payload.dict(exclude_unset=True).items()}
    
    if not data:
            raise HTTPException(status_code=400, detail="Nenhum campo válido enviado para atualização")
    
    response = supabase.table("crypto_settings").update(data).eq("id", id).execute()
    return getattr(response, "data", None)
  except Exception as e:
    err_str = e.args[0] if e.args else str(e)
    err_obj = ast.literal_eval(err_str)
    message = err_obj.get("message", str(e))

    raise HTTPException(status_code=400, detail=message)