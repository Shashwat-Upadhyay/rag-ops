export PYTHONPATH := src:.

pipeline:   ## build index, track experiments in MLflow, register best model
	python -m ragops.pipeline

api:        ## start the FastAPI backend on :8000
	uvicorn api.main:app --reload --port 8000

ui:         ## start the Streamlit frontend on :8501
	streamlit run frontend/Employee_Assistant.py

stop:       ## stop all running backend (:8000) and frontend (:8501) services
	py -3.12 stop_project.py

mlflow:     ## MLflow UI on :5000
	mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000

test:
	pytest -q

lint:
	ruff check .
