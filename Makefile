.PHONY: help setup data clean lint test train predict explore convert mlflow-ui

help:
	@echo "Available commands:"
	@echo "  make setup     - Set up the development environment"
	@echo "  make convert   - Convert Excel data to CSV (one-time setup)"
	@echo "  make data      - Process raw data into features"
	@echo "  make train     - Train the model"
	@echo "  make predict   - Make predictions with trained model"
	@echo "  make explore   - Run exploratory data analysis"
	@echo "  make mlflow-ui - Start MLflow UI with SQLite backend"
	@echo "  make clean     - Remove generated files"
	@echo "  make lint      - Run code linters"
	@echo "  make test      - Run tests"

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

