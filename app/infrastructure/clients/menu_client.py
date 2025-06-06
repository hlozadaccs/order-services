from threading import Lock

import grpc

from app.infrastructure.clients.menu_grpc import menu_pb2, menu_pb2_grpc


class MenuClientSingleton:
    _instance = None
    _lock: Lock = Lock()

    def __new__(cls, host: str = "127.0.0.1", port: int = 50051):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(MenuClientSingleton, cls).__new__(cls)
                    cls._instance._init_grpc_stub(host, port)
        return cls._instance

    def _init_grpc_stub(self, host: str, port: int):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = menu_pb2_grpc.MenuServiceStub(self.channel)

    def get_menu_item(self, item_id: int):
        request = menu_pb2.GetMenuItemRequest(id=item_id)
        response = self.stub.GetMenuItem(request)
        return response.item

    def list_menu_items(self):
        request = menu_pb2.ListMenuItemsRequest()
        response = self.stub.ListMenuItems(request)
        return response.items
