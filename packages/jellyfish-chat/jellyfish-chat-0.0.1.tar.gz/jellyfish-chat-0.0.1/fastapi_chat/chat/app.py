from datetime import datetime

import sentry_sdk
from fastapi import Depends, FastAPI, HTTPException, WebSocket
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.websockets import WebSocketDisconnect
from websockets.exceptions import ConnectionClosedOK

from .manager import connection_manager
from .redis_connector import connect_redis
from .settings import (
    BrokerSettings,
    DjangoServerSettings,
    GlobalSettings,
    get_broker_settings,
    get_django_settings,
    get_global_settings,
)


sentry_sdk.init(
    dsn=get_global_settings().sentry_dsn,
    environment=get_global_settings().environment,
)
app = FastAPI()

try:
    app.add_middleware(SentryAsgiMiddleware)
except:
    # pass silently if the Sentry integration failed
    pass


@app.on_event("startup")
async def startup_event():
    redis = await connect_redis()
    app.state.redis = redis


@app.websocket("/chat")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str,
    django_settings: DjangoServerSettings = Depends(get_django_settings),
    broker_settings: BrokerSettings = Depends(get_broker_settings),
    global_settings: GlobalSettings = Depends(get_global_settings),
):
    user_id = await connection_manager.check_auth(token, django_settings)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    await connection_manager.connect(websocket, user_id)
    if global_settings.capture_messages:
        sentry_sdk.capture_message(
            f"{datetime.now()}, successfully connected user {user_id}",
            level="info",
        )

    (channel,) = await app.state.redis.subscribe(broker_settings.channel_name)
    try:
        while await channel.wait_message():
            msg = await channel.get()
            if global_settings.capture_messages:
                sentry_sdk.capture_message(
                    f"{datetime.now()}, new message from subscriber {msg}"
                )
            await connection_manager.broadcast(msg)
    except WebSocketDisconnect as exc:
        if global_settings.capture_messages:
            sentry_sdk.capture_message(
                f"{datetime.now()}, exception websocket disconnect {exc}"
            )
    except ConnectionClosedOK as exc:
        if global_settings.capture_messages:
            sentry_sdk.capture_message(
                f"{datetime.now()}, exception closed OK {exc}"
            )
    finally:
        channel.close()
        await connection_manager.disconnect(websocket)
