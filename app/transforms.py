from typing import Any

import jmespath


def apply_transform_jmes(data: Any, expr: str | None, meta: dict[str, Any]) -> Any:
    if not expr:
        return data
    # Provide a helper function namespace by injecting meta into data
    # Wrap data with {"meta": meta, **original}
    augmented = {"meta": meta, **data} if isinstance(data, dict) else {"meta": meta, "data": data}
    try:
        return jmespath.search(expr, augmented)
    except Exception:
        return data  # fail-open: return original data


