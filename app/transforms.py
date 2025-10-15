from typing import Any, Optional

import jmespath


def apply_transform_jmes(data: Any, expr: Optional[str], meta: dict[str, Any]) -> Any:
    if not expr:
        return data
    # Provide a helper function namespace by injecting meta into data
    # Wrap data with {"meta": meta, **original}
    if isinstance(data, dict):
        augmented = {"meta": meta, **data}
    else:
        augmented = {"meta": meta, "data": data}
    try:
        return jmespath.search(expr, augmented)
    except Exception:
        return data  # fail-open: return original data


