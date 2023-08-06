from datetime import datetime

import sentry_sdk
from broadcaster import Broadcast
from fastapi import Depends, FastAPI, HTTPException, WebSocket
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from websockets.exceptions import ConnectionClosedOK

from .manager import connection_manager
from .settings import (
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
broker_settings = get_broker_settings()
broadcast = Broadcast(
    f"redis://{broker_settings.host}:{broker_settings.port}/{broker_settings.db}"
)
app = FastAPI(
    on_startup=[broadcast.connect], on_shutdown=[broadcast.disconnect]
)

try:
    app.add_middleware(SentryAsgiMiddleware)
except:
    # pass silently if the Sentry integration failed
    pass


@app.websocket("/chat")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str,
    django_settings: DjangoServerSettings = Depends(get_django_settings),
    global_settings: GlobalSettings = Depends(get_global_settings),
):
    user_id = await connection_manager.check_auth(token, django_settings)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    await connection_manager.connect(websocket)
    if global_settings.capture_messages:
        sentry_sdk.capture_message(
            f"{datetime.now()}, successfully connected user {user_id}",
            level="info",
        )

    try:
        async with broadcast.subscribe(channel="chat_channel") as subscriber:
            async for event in subscriber:
                await connection_manager.send_if_needed(msg=event.message, user_id=user_id, websocket=websocket)
    except ConnectionClosedOK as exc:
        if global_settings.capture_messages:
            sentry_sdk.capture_message(
                f"{datetime.now()}, exception closed OK {exc}"
            )
