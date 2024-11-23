from typing import List, Optional, Dict, Union
from uuid import uuid4
from datetime import datetime
from app.schema.response_schema import ResponseModel, PaginationMeta
from fastapi import Request, HTTPException, status

class APIResponse:
    @staticmethod
    def generate_metadata(request: Optional[Request] = None) -> Dict[str, str]:
        
        return {
            "request_id": str(uuid4()),
            "timestamp": datetime.now().isoformat(),
            "client": request.client.host if request else "Unknown"
        }

    @staticmethod
    def success(
        code: int = status.HTTP_200_OK,
        message: str = "Request processed successfully.",
        result: Optional[Union[Dict, List]] = None,
        meta: Optional[Union[Dict, PaginationMeta]] = None
    ) -> ResponseModel:
        
        return ResponseModel(
            code=code,
            message=message,
            result=result,
            meta=meta,
            errors=None
        )

    @staticmethod
    def error(
        code: int,
        message: str,
        errors: Optional[Dict[str, str]] = None,
        meta: Optional[Dict[str, str]] = None
    ) -> None:
        
        raise HTTPException(
            status_code=code,
            detail={
                "message": message,
                "errors": errors,
                "meta": meta
            }
        )

    @staticmethod
    def paginate(
        data: List[Dict],
        page: int,
        per_page: int
    ) -> Dict[str, Union[List[Dict], PaginationMeta]]:
        
        total_items = len(data)
        total_pages = (total_items + per_page - 1) // per_page 

        if page < 1 or page > total_pages:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Page number out of range."
            )

        start_index = (page - 1) * per_page
        end_index = start_index + per_page

        paginated_data = data[start_index:end_index]

        return {
            "result": paginated_data,
            "meta": {
                "pagination": PaginationMeta(
                    current_page=page,
                    per_page=per_page,
                    total_pages=total_pages,
                    total_items=total_items
                ).dict()
            }
        }
