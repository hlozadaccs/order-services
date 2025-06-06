PROTO_SRC=protos
PROTO_GEN_PYTHON=app/infrastructure/clients/menu_grpc

.PHONY: proto-gen proto-clean

proto-gen:
	mkdir -p $(PROTO_GEN_PYTHON)
	poetry run python -m grpc_tools.protoc \
		-I $(PROTO_SRC) \
		--python_out=$(PROTO_GEN_PYTHON) \
		--grpc_python_out=$(PROTO_GEN_PYTHON) \
		--mypy_out=$(PROTO_GEN_PYTHON) \
		$(PROTO_SRC)/menu.proto
	@# Fix imports - Versión compatible universal
	@if [ -f "$(PROTO_GEN_PYTHON)/menu_pb2_grpc.py" ]; then \
		sed -i.bak 's/^import menu_pb2/from app.infrastructure.clients.menu_grpc import menu_pb2/' $(PROTO_GEN_PYTHON)/menu_pb2_grpc.py; \
		rm -f $(PROTO_GEN_PYTHON)/menu_pb2_grpc.py.bak; \
	fi

proto-clean:
	rm -rf $(PROTO_GEN_PYTHON)
