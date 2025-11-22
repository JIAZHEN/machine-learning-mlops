.PHONY: help setup data clean lint test train predict explore convert mlflow-ui api drift-monitor docker-build docker-run k8s-deploy k8s-delete

help:
	@echo "Available commands:"
	@echo "  make setup          - Set up the development environment"
	@echo "  make convert        - Convert Excel data to CSV (one-time setup)"
	@echo "  make data           - Process raw data into features"
	@echo "  make train          - Train the model"
	@echo "  make predict        - Make predictions with trained model"
	@echo "  make explore        - Run exploratory data analysis"
	@echo "  make mlflow-ui      - Start MLflow UI with SQLite backend"
	@echo "  make api            - Start FastAPI prediction service"
	@echo "  make drift-monitor  - Run data drift monitoring"
	@echo "  make docker-build   - Build Docker image"
	@echo "  make docker-run     - Run Docker container locally"
	@echo "  make k8s-deploy     - Deploy to Kubernetes"
	@echo "  make k8s-delete     - Delete Kubernetes deployment"
	@echo "  make clean          - Remove generated files"
	@echo "  make lint           - Run code linters"
	@echo "  make test           - Run tests"

setup:
	pip install -r requirements.txt

convert:
	@echo "Converting Excel to CSV..."
	python scripts/convert_xlsx_to_csv.py

data:
	@echo "Processing data pipeline..."
	python src/pipeline.py

train:
	@echo "Training model..."
	python src/models/model1/train.py

predict:
	@echo "Making predictions..."
	python src/models/model1/predict.py

explore:
	@echo "Running exploratory data analysis..."
	python -m src.visualization.exploration

mlflow-ui:
	@echo "Starting MLflow UI with SQLite backend..."
	@echo "Access at: http://localhost:5000"
	mlflow ui --backend-store-uri sqlite:///mlflow.db

api:
	@echo "Starting FastAPI prediction service..."
	@echo "Access at: http://localhost:8000"
	@echo "API docs: http://localhost:8000/docs"
	python src/api/app.py

drift-monitor:
	@echo "Running data drift monitoring..."
	python src/monitoring/drift_monitor.py

docker-build:
	@echo "Building Docker image..."
	docker build -t churn-prediction:1.0.0 .
	@echo "Image built successfully: churn-prediction:1.0.0"

docker-run:
	@echo "Running Docker container..."
	docker run -d \
		--name churn-api \
		-p 8000:8000 \
		-v $(PWD)/models:/app/models:ro \
		churn-prediction:1.0.0
	@echo "Container started. Access at http://localhost:8000"
	@echo "View logs: docker logs -f churn-api"
	@echo "Stop: docker stop churn-api && docker rm churn-api"

docker-stop:
	@echo "Stopping Docker container..."
	docker stop churn-api || true
	docker rm churn-api || true

k8s-deploy:
	@echo "Deploying to Kubernetes..."
	kubectl apply -f k8s/namespace.yaml
	kubectl apply -f k8s/configmap.yaml
	kubectl apply -f k8s/rbac.yaml
	kubectl apply -f k8s/pvc.yaml
	kubectl apply -f k8s/deployment.yaml
	kubectl apply -f k8s/service.yaml
	kubectl apply -f k8s/hpa.yaml
	@echo "Deployment complete!"
	@echo "Check status: kubectl get pods -n ml-production"

k8s-delete:
	@echo "Deleting Kubernetes resources..."
	kubectl delete -f k8s/hpa.yaml || true
	kubectl delete -f k8s/service.yaml || true
	kubectl delete -f k8s/deployment.yaml || true
	kubectl delete -f k8s/pvc.yaml || true
	kubectl delete -f k8s/rbac.yaml || true
	kubectl delete -f k8s/configmap.yaml || true
	@echo "Resources deleted!"

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info

lint:
	flake8 src/
	pylint src/

test:
	pytest tests/

