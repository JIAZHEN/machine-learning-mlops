"""
FastAPI application for churn prediction service.

Production-ready REST API with:
- Health checks
- Model versioning
- Request validation
- Error handling
- Logging
- Prometheus metrics
"""
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator, ConfigDict
import pandas as pd
import uvicorn

# Add src to path for imports
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root / "src" / "models" / "model1"))

from predict import ChurnPredictor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global predictor instance
predictor: Optional[ChurnPredictor] = None


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan (startup/shutdown)."""
    # Startup
    global predictor
    try:
        logger.info("Loading model and preprocessor...")
        predictor = ChurnPredictor()
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        predictor = None
    
    yield
    
    # Shutdown
    logger.info("Shutting down API...")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Churn Prediction API",
    description="Production-ready API for telecom customer churn prediction",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response validation
class CustomerFeatures(BaseModel):
    """Customer features for prediction."""
    
    # Demographics
    gender: str = Field(..., description="Gender (Male/Female)")
    SeniorCitizen: int = Field(..., ge=0, le=1, description="Senior citizen flag (0/1)")
    Partner: str = Field(..., description="Has partner (Yes/No)")
    Dependents: str = Field(..., description="Has dependents (Yes/No)")
    
    # Service information
    tenure: int = Field(..., ge=0, description="Months with company")
    PhoneService: str = Field(..., description="Has phone service (Yes/No)")
    MultipleLines: str = Field(..., description="Has multiple lines (Yes/No/No phone service)")
    InternetService: str = Field(..., description="Internet service type (DSL/Fiber optic/No)")
    OnlineSecurity: str = Field(..., description="Has online security (Yes/No/No internet service)")
    OnlineBackup: str = Field(..., description="Has online backup (Yes/No/No internet service)")
    DeviceProtection: str = Field(..., description="Has device protection (Yes/No/No internet service)")
    TechSupport: str = Field(..., description="Has tech support (Yes/No/No internet service)")
    StreamingTV: str = Field(..., description="Has streaming TV (Yes/No/No internet service)")
    StreamingMovies: str = Field(..., description="Has streaming movies (Yes/No/No internet service)")
    
    # Contract information
    Contract: str = Field(..., description="Contract type (Month-to-month/One year/Two year)")
    PaperlessBilling: str = Field(..., description="Has paperless billing (Yes/No)")
    PaymentMethod: str = Field(..., description="Payment method")
    MonthlyCharges: float = Field(..., ge=0, description="Monthly charges in dollars")
    TotalCharges: float = Field(..., ge=0, description="Total charges in dollars")
    
    @field_validator('gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 
                     'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                     'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 
                     'PaperlessBilling', 'PaymentMethod')
    @classmethod
    def validate_categorical(cls, v: str) -> str:
        """Validate categorical fields are not empty."""
        if not v or v.strip() == "":
            raise ValueError("Field cannot be empty")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "gender": "Female",
                "SeniorCitizen": 0,
                "Partner": "Yes",
                "Dependents": "No",
                "tenure": 12,
                "PhoneService": "Yes",
                "MultipleLines": "No",
                "InternetService": "Fiber optic",
                "OnlineSecurity": "No",
                "OnlineBackup": "Yes",
                "DeviceProtection": "No",
                "TechSupport": "No",
                "StreamingTV": "Yes",
                "StreamingMovies": "No",
                "Contract": "Month-to-month",
                "PaperlessBilling": "Yes",
                "PaymentMethod": "Electronic check",
                "MonthlyCharges": 70.35,
                "TotalCharges": 840.20
            }
        }
    )


class PredictionRequest(BaseModel):
    """Request model for predictions."""
    customers: List[CustomerFeatures] = Field(..., min_length=1, max_length=1000)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "customers": [CustomerFeatures.model_config["json_schema_extra"]["example"]]
            }
        }
    )


class PredictionResponse(BaseModel):
    """Response model for predictions."""
    predictions: List[Dict]
    model_version: str
    timestamp: str


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    model_loaded: bool
    timestamp: str
    version: str


# Health check endpoints
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint."""
    return {
        "message": "Churn Prediction API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint for Kubernetes liveness/readiness probes.
    """
    return HealthResponse(
        status="healthy" if predictor is not None else "unhealthy",
        model_loaded=predictor is not None,
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0"
    )


@app.get("/ready", tags=["Health"])
async def readiness_check():
    """
    Readiness check for Kubernetes.
    Returns 200 if model is loaded and ready.
    """
    if predictor is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    return {"status": "ready", "timestamp": datetime.utcnow().isoformat()}


# Prediction endpoints
@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(request: PredictionRequest):
    """
    Make churn predictions for one or more customers.
    
    Returns prediction (0=no churn, 1=churn) and probability for each customer.
    """
    if predictor is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded. Please check service health."
        )
    
    try:
        # Convert request to DataFrame
        customers_data = [customer.dict() for customer in request.customers]
        df = pd.DataFrame(customers_data)
        
        # Make predictions
        results = predictor.predict(df)
        
        # Format response
        predictions = []
        for idx, (pred, prob) in enumerate(zip(results['prediction'], results['churn_probability'])):
            predictions.append({
                "customer_index": idx,
                "will_churn": bool(pred),
                "churn_probability": round(float(prob), 4),
                "risk_level": _get_risk_level(float(prob))
            })
        
        logger.info(f"Predicted {len(predictions)} customers")
        
        return PredictionResponse(
            predictions=predictions,
            model_version="1.0.0",
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@app.post("/predict/single", tags=["Prediction"])
async def predict_single(customer: CustomerFeatures):
    """
    Make churn prediction for a single customer.
    Convenience endpoint for single predictions.
    """
    if predictor is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    try:
        result = predictor.predict_single(customer.dict())
        result['risk_level'] = _get_risk_level(result['churn_probability'])
        result['churn_probability'] = round(result['churn_probability'], 4)
        result['timestamp'] = datetime.utcnow().isoformat()
        
        logger.info(f"Single prediction: churn={result['will_churn']}, prob={result['churn_probability']}")
        
        return result
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


# Helper functions
def _get_risk_level(probability: float) -> str:
    """Categorize churn probability into risk levels."""
    if probability < 0.3:
        return "low"
    elif probability < 0.6:
        return "medium"
    else:
        return "high"


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    reload = os.getenv("API_RELOAD", "false").lower() == "true"
    
    logger.info(f"Starting API server on {host}:{port}")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

