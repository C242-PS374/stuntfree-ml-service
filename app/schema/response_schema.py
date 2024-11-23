from pydantic import BaseModel
from typing import Optional, Dict, Union, List

class PaginationMeta(BaseModel):
    current_page: int
    per_page: int
    total_pages: int
    total_items: int

class ResponseModel(BaseModel):
    code: int
    message: str
    result: Optional[Union[Dict, List]] = None
    meta: Optional[Union[Dict, PaginationMeta]] = None
    errors: Optional[Dict[str, str]] = None
