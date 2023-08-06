from typing import Dict
from typing import List

__virtualname__ = "json"


async def delete(
    hub,
    ctx,
    url: str,
    headers: Dict[str, str] = None,
    success_codes: List[int] = None,
    **kwargs,
):
    if not success_codes:
        success_codes = [200]
    if not headers:
        headers = {}
    if not headers.get("content-type"):
        headers["content-type"] = "application/json"

    async with await hub.tool.request.session.delete(
        ctx, url=url, headers=headers, **kwargs
    ) as response:
        success = response.status in success_codes
        if success:
            ret = hub.tool.type.dict.namespaced(await response.json())
        else:
            ret = await response.read()
            hub.log.debug(f"Delete error: {ret}".strip())
            ret = ret.decode() if hasattr(ret, "decode") else ret
        return {
            "ret": ret,
            "result": success,
            "status": response.status,
            "comment": response.reason,
            "headers": response.headers,
        }


async def get(
    hub,
    ctx,
    url: str,
    headers: Dict[str, str] = None,
    success_codes: List[int] = None,
    **kwargs,
):
    if not success_codes:
        success_codes = [200]
    if not headers:
        headers = {}
    if not headers.get("content-type"):
        headers["content-type"] = "application/json"

    async with await hub.tool.request.session.get(
        ctx, url=url, headers=headers, **kwargs
    ) as response:
        success = response.status in success_codes
        if success:
            ret = hub.tool.type.dict.namespaced(await response.json())
        else:
            ret = await response.read()
            hub.log.debug(f"Get error: {ret}".strip())
            ret = ret.decode() if hasattr(ret, "decode") else ret
        return {
            "ret": ret,
            "result": success,
            "status": response.status,
            "comment": response.reason,
            "headers": response.headers,
        }


async def head(
    hub,
    ctx,
    url: str,
    headers: Dict[str, str] = None,
    success_codes: List[int] = None,
    **kwargs,
):
    if not success_codes:
        success_codes = [200]
    if not headers:
        headers = {}
    if not headers.get("content-type"):
        headers["content-type"] = "application/json"

    async with await hub.tool.request.session.head(
        ctx, url=url, headers=headers, **kwargs
    ) as response:
        success = response.status in success_codes
        if success:
            ret = hub.tool.type.dict.namespaced(await response.json())
        else:
            ret = await response.read()
            hub.log.debug(f"Head error: {ret}".strip())
            ret = ret.decode() if hasattr(ret, "decode") else ret
        return {
            "ret": ret,
            "result": success,
            "status": response.status,
            "comment": response.reason,
            "headers": response.headers,
        }


async def patch(
    hub,
    ctx,
    url: str,
    headers: Dict[str, str] = None,
    success_codes: List[int] = None,
    **kwargs,
):
    if not success_codes:
        success_codes = [200]
    if not headers:
        headers = {}

    if not headers.get("content-type"):
        headers["content-type"] = "application/json"

    async with await hub.tool.request.session.patch(
        ctx, url=url, headers=headers, **kwargs
    ) as response:
        success = response.status in success_codes
        if success:
            ret = hub.tool.type.dict.namespaced(await response.json())
        else:
            ret = await response.read()
            hub.log.debug(f"Patch error: {ret}".strip())
            ret = ret.decode() if hasattr(ret, "decode") else ret
        return {
            "ret": ret,
            "result": success,
            "status": response.status,
            "comment": response.reason,
            "headers": response.headers,
        }


async def post(
    hub,
    ctx,
    url: str,
    headers: Dict[str, str] = None,
    success_codes: List[int] = None,
    **kwargs,
):
    if not success_codes:
        success_codes = [200]
    if not headers:
        headers = {}
    if not headers.get("content-type"):
        headers["content-type"] = "application/json"

    async with await hub.tool.request.session.post(
        ctx, url=url, headers=headers, **kwargs
    ) as response:
        success = response.status in success_codes
        if success:
            ret = hub.tool.type.dict.namespaced(await response.json())
        else:
            ret = await response.read()
            hub.log.debug(f"Post error: {ret}".strip())
            ret = ret.decode() if hasattr(ret, "decode") else ret
        return {
            "ret": ret,
            "result": success,
            "status": response.status,
            "comment": response.reason,
            "headers": response.headers,
        }


async def put(
    hub,
    ctx,
    url: str,
    headers: Dict[str, str] = None,
    success_codes: List[int] = None,
    **kwargs,
):
    if not success_codes:
        success_codes = [200]
    if not headers:
        headers = {}

    headers["content-type"] = "application/json"
    async with await hub.tool.request.session.put(
        ctx, url=url, headers=headers, **kwargs
    ) as response:
        success = response.status in success_codes
        if success:
            ret = hub.tool.type.dict.namespaced(await response.json())
        else:
            ret = await response.read()
            hub.log.debug(f"Put error: {ret}".strip())
            ret = ret.decode() if hasattr(ret, "decode") else ret
        return {
            "ret": ret,
            "result": success,
            "status": response.status,
            "comment": response.reason,
            "headers": response.headers,
        }
