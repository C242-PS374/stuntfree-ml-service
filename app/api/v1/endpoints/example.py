from fastapi import APIRouter, Query, Request

from app.schema.response_schema import ResponseModel
from app.util.response_format import APIResponse

router = APIRouter(prefix="/example", tags=["Example"])

mock_items = [{"id": i, "name": f"Item {i}"} for i in range(1, 101)]

@router.get("/items", response_model=ResponseModel)
def get_paginated_items(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    request: Request = None
):
    
    pagination_result = APIResponse.paginate(mock_items, page, per_page)
    metadata = APIResponse.generate_metadata(request)
    combined_meta = {**metadata, **pagination_result["meta"]}

    return APIResponse.success(
        result=pagination_result["result"],
        meta=combined_meta,
        message="Items retrieved successfully."
    )

@router.get("/custom-success", response_model=ResponseModel)
def custom_success_response(request: Request = None):
    
    metadata = APIResponse.generate_metadata(request)
    custom_meta = {**metadata, "custom_field": "Custom Value"}

    return APIResponse.success(
        result={"key": "value", "example": "Custom success response"},
        meta=custom_meta,
        message="Custom success message."
    )

@router.get("/error-example", response_model=ResponseModel)
def simulate_error():
    
    return APIResponse.error(
        code=400,
        message="Invalid request parameters.",
        errors={"parameter": "The 'page' parameter must be greater than 0."},
        meta={"info": "This error occurred due to invalid input."}
    )

@router.get("/conditional-response", response_model=ResponseModel)
def conditional_response(condition: str, request: Request = None):
    
    metadata = APIResponse.generate_metadata(request)

    if condition == "success":
        return APIResponse.success(
            result={"status": "success"},
            meta=metadata,
            message="Condition met successfully."
        )
    elif condition == "error":
        return APIResponse.error(
            code=422,
            message="Unprocessable condition provided.",
            errors={"condition": f"Invalid condition '{condition}'"},
            meta=metadata
        )
    else:
        return APIResponse.success(
            result={"status": "neutral"},
            meta=metadata,
            message="Neutral condition processed."
        )

@router.get("/health", response_model=ResponseModel)
def health_check(request: Request = None):
    
    metadata = APIResponse.generate_metadata(request)
    health_status = {
        "service": "Example API Service",
        "status": "healthy"
    }

    return APIResponse.success(
        result=health_status,
        meta=metadata,
        message="System is healthy."
    )
