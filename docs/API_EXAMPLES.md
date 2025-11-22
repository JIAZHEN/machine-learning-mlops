# Quick Start API Examples

## Start the API

```bash
# Make sure you've trained the model first
make train

# Start the FastAPI service
make api
```

## Test the API

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-11-22T12:00:00",
  "version": "1.0.0"
}
```

### 2. Single Customer Prediction

```bash
curl -X POST http://localhost:8000/predict/single \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

Response:
```json
{
  "will_churn": true,
  "churn_probability": 0.7845,
  "risk_level": "high",
  "timestamp": "2025-11-22T12:00:00"
}
```

### 3. Batch Predictions

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "customers": [
      {
        "gender": "Male",
        "SeniorCitizen": 1,
        "Partner": "No",
        "Dependents": "No",
        "tenure": 1,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "DSL",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 29.85,
        "TotalCharges": 29.85
      },
      {
        "gender": "Female",
        "SeniorCitizen": 0,
        "Partner": "Yes",
        "Dependents": "Yes",
        "tenure": 72,
        "PhoneService": "Yes",
        "MultipleLines": "Yes",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "Yes",
        "OnlineBackup": "Yes",
        "DeviceProtection": "Yes",
        "TechSupport": "Yes",
        "StreamingTV": "Yes",
        "StreamingMovies": "Yes",
        "Contract": "Two year",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Bank transfer (automatic)",
        "MonthlyCharges": 118.75,
        "TotalCharges": 8546.75
      }
    ]
  }'
```

Response:
```json
{
  "predictions": [
    {
      "customer_index": 0,
      "will_churn": true,
      "churn_probability": 0.8234,
      "risk_level": "high"
    },
    {
      "customer_index": 1,
      "will_churn": false,
      "churn_probability": 0.1256,
      "risk_level": "low"
    }
  ],
  "model_version": "1.0.0",
  "timestamp": "2025-11-22T12:00:00"
}
```

## Python Client Example

```python
import requests
import json

# API endpoint
API_URL = "http://localhost:8000"

# Customer data
customer = {
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

# Make prediction
response = requests.post(
    f"{API_URL}/predict/single",
    json=customer,
    headers={"Content-Type": "application/json"}
)

# Print result
result = response.json()
print(f"Will churn: {result['will_churn']}")
print(f"Probability: {result['churn_probability']:.2%}")
print(f"Risk level: {result['risk_level']}")
```

## Interactive API Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation where you can:
- See all available endpoints
- Try out API calls directly in the browser
- View request/response schemas
- Download OpenAPI specification

## Risk Levels

The API categorizes churn probability into risk levels:

| Probability | Risk Level | Action |
|-------------|-----------|---------|
| < 30% | **Low** | Standard monitoring |
| 30-60% | **Medium** | Proactive engagement |
| > 60% | **High** | Immediate retention offer |

## Rate Limiting

The API is configured with:
- Max 100 requests per minute per IP
- Max 1000 customers per batch request

## Error Handling

### 400 Bad Request
Missing or invalid customer data:
```json
{
  "detail": "Field validation error: tenure must be >= 0"
}
```

### 503 Service Unavailable
Model not loaded:
```json
{
  "detail": "Model not loaded. Please check service health."
}
```

### 500 Internal Server Error
Prediction error:
```json
{
  "detail": "Prediction failed: [error details]"
}
```

