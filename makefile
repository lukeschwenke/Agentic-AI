
APP_NAME=Agentic_Refinance_Tool
IMAGE_NAME=agentic_refinance_tool_image
CONTAINER_NAME=agentic_refinace_tool_container
PORT=8000

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -d --name $(CONTAINER_NAME) --env-file .env -p $(PORT):8000 $(IMAGE_NAME)

ui:
	poetry run streamlit run src/frontend/Agentic_Refinance_Tool.py

stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

#restart: stop run
go: build run ui
rebuild: stop build run ui


# docker build -t refinance_tool .
# docker run --name refinance_api --env-file .env -p 8000:8000 refinance_tool