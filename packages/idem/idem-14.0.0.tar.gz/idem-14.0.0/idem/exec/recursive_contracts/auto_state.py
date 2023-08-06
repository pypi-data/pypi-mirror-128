"""
If an exec module plugin implements this contract,
the same ref can be used to call the state functions "present", "absent", and "describe".
"""
from typing import Any
from typing import Dict


async def sig_get(hub, ctx, name, **kwargs) -> Dict[str, Any]:
    return {"result": True | False, "comment": "", "ret": None}


async def sig_list(hub, ctx) -> Dict[str, Any]:
    return {"result": True | False, "comment": "", "ret": None}


async def sig_create(hub, ctx, name, **kwargs) -> Dict[str, Any]:
    return {"result": True | False, "comment": "", "ret": None}


async def sig_update(hub, ctx, name, **kwargs) -> Dict[str, Any]:
    return {"result": True | False, "comment": "", "ret": None}


async def sig_delete(hub, ctx, name, **kwargs) -> Dict[str, Any]:
    return {"result": True | False, "comment": "", "ret": None}
