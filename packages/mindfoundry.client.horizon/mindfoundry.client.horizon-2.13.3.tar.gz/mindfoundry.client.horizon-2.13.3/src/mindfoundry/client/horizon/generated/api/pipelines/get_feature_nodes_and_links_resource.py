from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.feature_nodes_and_links import FeatureNodesAndLinks
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    id: int,
    stage_id: int,
) -> Dict[str, Any]:
    url = "{}/pipelines/{id}/stages/{stageId}/features/graph".format(
        client.base_url, id=id, stageId=stage_id
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[FeatureNodesAndLinks]:
    if response.status_code == 200:
        response_200 = FeatureNodesAndLinks.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[FeatureNodesAndLinks]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    id: int,
    stage_id: int,
) -> Response[FeatureNodesAndLinks]:
    kwargs = _get_kwargs(
        client=client,
        id=id,
        stage_id=stage_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    id: int,
    stage_id: int,
) -> Optional[FeatureNodesAndLinks]:
    """  """

    return sync_detailed(
        client=client,
        id=id,
        stage_id=stage_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    id: int,
    stage_id: int,
) -> Response[FeatureNodesAndLinks]:
    kwargs = _get_kwargs(
        client=client,
        id=id,
        stage_id=stage_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    id: int,
    stage_id: int,
) -> Optional[FeatureNodesAndLinks]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            id=id,
            stage_id=stage_id,
        )
    ).parsed
