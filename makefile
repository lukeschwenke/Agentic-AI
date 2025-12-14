
APP_NAME=Agentic_Refinance_Tool
IMAGE_NAME=agentic_refinance_tool_image
CONTAINER_NAME=agentic_refinace_tool_container
PORT=8000
PLATFORM=linux/amd64

AWS_REGION=us-east-1
AWS_ACCOUNT_ID=176276968777
ECR_REPO=datascience/agentic-ai-mortgage-refinance-tool
ECR_URI=$(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(ECR_REPO)
IMAGE_TAG=latest

build:
	docker buildx build \
		--platform $(PLATFORM) \
		-t $(IMAGE_NAME) \
		--load .

run:
	docker run -d \
		--name $(CONTAINER_NAME) \
		--env-file .env \
		-p $(PORT):8000 \
		$(IMAGE_NAME)

ui:
	poetry run streamlit run src/frontend/Agentic_Refinance_Tool.py

stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

go: build run ui
rebuild: stop build run ui

# docker build -t refinance_tool .
# docker run --name refinance_api --env-file .env -p 8000:8000 refinance_tool


# -------- ECR --------

login-ecr:
	aws ecr get-login-password --region $(AWS_REGION) | \
	docker login --username AWS --password-stdin \
	$(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com

build-ecr:
	docker buildx build \
		--platform $(PLATFORM) \
		-t $(ECR_URI):$(IMAGE_TAG) \
		--push .

push-ecr: login-ecr build-ecr