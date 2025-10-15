from typing import Any

from pydantic import BaseModel, ValidationError


# Optional Pydantic validation for schema drift detection
def validate_response(model: type[BaseModel] | None, data: Any) -> str | None:
    if not model:
        return None
    try:
        model.model_validate(data)
        return None
    except ValidationError as e:
        return str(e)


