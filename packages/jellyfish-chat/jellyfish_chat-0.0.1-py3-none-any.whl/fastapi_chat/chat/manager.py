import json
from dataclasses import dataclass
from typing import Optional

import httpx
from fastapi import WebSocket

from .settings import DjangoServerSettings


@dataclass
class Connection:
    user_id: int
    websocket: WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections.append(Connection(user_id, websocket))

    async def disconnect(self, websocket: WebSocket):
        await websocket.close()
        self.active_connections = list(
            filter(
                lambda connection: connection.websocket != websocket,
                self.active_connections,
            )
        )

    async def broadcast(self, msg: bytes):
        """
        Sends via websocket json, if it directed to current user
        (user's id is sender's id or in receivers' ids)
        """
        msg = json.loads(msg.decode("utf-8"))
        receiver_ids = msg.get("receiver_ids", [])
        sender_id = msg.get("sender_id")
        for connection in self.active_connections:
            if (
                connection.user_id == sender_id
                or connection.user_id in receiver_ids
            ):
                message_obj = msg.get("message", {})
                await connection.websocket.send_json(message_obj)

    @staticmethod
    async def check_auth(
        token: str, django_settings: DjangoServerSettings
    ) -> Optional[int]:
        """
        Sends request to django server with token to ensure connection and get user's id.
        """
        async with httpx.AsyncClient() as client:
            token = f"{django_settings.token_type} {token}"
            response = await client.get(
                django_settings.get_user_url, headers={"Authorization": token}
            )
        if response.status_code == 200:
            return response.json().get(django_settings.user_response_id_field)


connection_manager = ConnectionManager()
