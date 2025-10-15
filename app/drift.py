from typing import Any, Optional

from pydantic import BaseModel, ValidationError


# Optional Pydantic validation for schema drift detection
def validate_response(model: Optional[type[BaseModel]], data: Any) -> Optional[str]:
    if not model:
        return None
    try:
        model.model_validate(data)
        return None
    except ValidationError as e:
        return str(e)


