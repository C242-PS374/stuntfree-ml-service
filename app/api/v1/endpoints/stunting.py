from fastapi import APIRouter, Query, Request

from app.schema.response_schema import ResponseModel
from app.util.response_format import APIResponse

router = APIRouter(prefix="/stunting", tags=["Stunting"])