from typing import List


async def delete(hub, ctx, url: str, success_codes: List[int] = None, **kwargs):
    if not success_codes:
        success_codes = [200]
    async with await hub.tool.request.session.delete(
        ctx, url=url, **kwargs
    ) as response:
        return {
            "ret": await response.read(),
            "result": response.status in success_codes,
            "status": response.status,
            "comment": response.reason,
            "headers": response.headers,
        }


async def get(hub, ctx, url: str, success_codes: List[int] = None, **kwargs):
    if not success_codes:
        success_codes = [200]
    async with await hub.tool.request.session.get(ctx, url=url, **kwargs) as response:
        return {
            "ret": await response.read(),
            "result": response.status in success_codes,
            "status": response.status,
            "comment": response.reason,
            "headers": response.headers,
        }


async def patch(hub, ctx, url: str, success_codes: List[int] = None, **kwargs):
    if not success_codes:
        success_codes = [200]
    async with await hub.tool.request.session.patch(ctx, url=url, **kwargs) as response:
        return {
            "ret": await response.read(),
            "result": response.status in success_codes,
            "status": response.status,
            "comment": response.reason,
            "headers": response.headers,
        }


async def post(hub, ctx, url: str, success_codes: List[int] = None, **kwargs):
    if not success_codes:
        success_codes = [200]
    async with await hub.tool.request.session.post(ctx, url=url, **kwargs) as response:
        return {
            "ret": await response.read(),
            "result": response.status in success_codes,
            "status": response.status,
            "comment": response.reason,
            "headers": response.headers,
        }


async def put(hub, ctx, url: str, success_codes: List[int] = None, **kwargs):
    if not success_codes:
        success_codes = [200]
    async with await hub.tool.request.session.put(ctx, url=url, **kwargs) as response:
        return {
            "ret": await response.read(),
            "result": response.status in success_codes,
            "status": response.status,
            "comment": response.reason,
            "headers": response.headers,
        }
