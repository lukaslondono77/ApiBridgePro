import time

# in-memory TTL cache: key -> (expires_at, content, headers, status)
_cache: dict[str, tuple[float, bytes, list[tuple[bytes, bytes]], int]] = {}

def get(key: str):
    ent = _cache.get(key)
    if not ent:
        return None
    exp, content, headers, status = ent
    if time.time() > exp:
        _cache.pop(key, None)
        return None
    return content, headers, status

def set(key: str, content: bytes, headers, status: int, ttl: int):
    _cache[key] = (time.time() + ttl, content, headers, status)


