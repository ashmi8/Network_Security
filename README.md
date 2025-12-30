# Network Security Project - Complete Documentation

## 📋 Table of Contents
1. Project Overview
2. Architecture & Workflow
3. Project Structure
4. Prerequisites & Setup
5. Installation & Configuration
6. Project Workflow
7. API Endpoints
8. Docker Setup
9. CI/CD Pipeline
10. Troubleshooting

---

## 🎯 Project Overview

**Network Security** is an end-to-end machine learning application designed to detect phishing and network security threats using classification models. The project implements a complete MLOps pipeline with data ingestion, validation, transformation, model training, and deployment capabilities.

### Key Features
- **Data Pipeline**: MongoDB integration for data ingestion
- **Data Validation**: Schema validation and drift detection
- **Data Transformation**: KNN imputation for missing values
- **Model Training**: Multiple classification algorithms with hyperparameter tuning
- **MLflow Integration**: Experiment tracking and model monitoring
- **REST API**: FastAPI for model serving and predictions
- **Cloud Integration**: AWS S3 for artifact storage
- **Docker Support**: Containerized deployment
- **CI/CD**: GitHub Actions for automated workflows

---

## 🏗️ Architecture & Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA SOURCE (MongoDB)                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│          1. DATA INGESTION (CSV Export & Split)             │
│  - Connects to MongoDB                                      │
│  - Exports collection as DataFrame                          │
│  - Splits into train/test sets (80/20)                      │
│  - Saves to: Artifacts/<timestamp>/data_ingestion/          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│       2. DATA VALIDATION (Schema & Drift Detection)         │
│  - Validates number of columns against schema.yaml          │
│  - Detects data drift using KS-2 sample test               │
│  - Generates drift report                                   │
│  - Saves valid data to: data_validation/validated/          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│    3. DATA TRANSFORMATION (Feature Engineering & Imputation)│
│  - Handles missing values with KNNImputer (k=3)             │
│  - Creates preprocessing pipeline                           │
│  - Transforms features using fitted preprocessor            │
│  - Saves transformed data as .npy files                     │
│  - Saves preprocessor object for inference                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│   4. MODEL TRAINING (Hyperparameter Tuning & Evaluation)    │
│  - Trains multiple algorithms:                              │
│    • Random Forest                                          │
│    • Decision Tree                                          │
│    • Gradient Boosting                                      │
│    • Logistic Regression                                    │
│    • AdaBoost                                               │
│  - GridSearchCV for hyperparameter optimization             │
│  - Evaluates on train/test sets                             │
│  - Calculates metrics: F1, Precision, Recall                │
│  - Tracks experiments with MLflow                           │
│  - Selects best model based on test R² score                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│        5. MODEL DEPLOYMENT (S3 & Final Model Creation)      │
│  - Saves artifacts to S3 bucket                             │
│  - Creates NetworkModel wrapper (preprocessor + model)      │
│  - Saves final_model/ directory with:                       │
│    • model.pkl (trained classifier)                         │
│    • preprocessor.pkl (transformation pipeline)             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              6. INFERENCE (REST API Endpoint)                │
│  - Load preprocessor and model from final_model/            │
│  - Create NetworkModel instance                             │
│  - Transform input features with preprocessor               │
│  - Generate predictions                                     │
│  - Return predictions to user                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Network_Security/
├── Network_security/
│   ├── components/
│   │   ├── data_ingestion.py          # MongoDB → CSV conversion
│   │   ├── data_validation.py         # Schema & drift validation
│   │   ├── data_transformation.py     # Feature preprocessing
│   │   └── model_trainer.py           # Model training & selection
│   ├── entity/
│   │   ├── config_entity.py           # Configuration classes
│   │   └── artifacts_entity.py        # Artifact data classes
│   ├── exception/
│   │   └── exception.py               # Custom exception handling
│   ├── logging/
│   │   └── logger.py                  # Logging configuration
│   ├── utils/
│   │   ├── main_utils/
│   │   │   └── utils.py               # Helper functions
│   │   └── ml_utils/
│   │       ├── metric/
│   │       │   └── classification_metric.py   # Metrics calculation
│   │       └── model/
│   │           └── estimator.py       # NetworkModel wrapper
│   ├── constants/
│   │   └── training_pipeline/
│   │       └── __init__.py            # Pipeline constants
│   ├── cloud/
│   │   └── s3_syncer.py               # AWS S3 integration
│   └── pipeline/
│       └── training_pipeline.py       # Main orchestration
├── data_schema/
│   └── schema.yaml                    # Data validation schema
├── templates/
│   └── table.html                     # HTML template for predictions
├── logs/                              # Training logs
├── Artifacts/                         # Generated artifacts
├── final_model/                       # Deployed model artifacts
├── prediction_output/                 # Prediction results
│
├── app.py                             # FastAPI application
├── main.py                            # Direct execution entry point
├── push_data.py                       # MongoDB data loader
│
├── requirements.txt                   # Python dependencies
├── setup.py                           # Package configuration
├── DOCKERFILE                         # Container configuration
├── .github/
│   └── workflows/
│       └── main.yml                   # GitHub Actions CI/CD
├── .env                               # Environment variables
├── .env.example                       # Environment template
├── .gitignore                         # Git ignore rules
├── LICENSE                            # GPL v3 License
└── README.md                          # This file
```

---

## 🔧 Installation & Configuration

### Step 1: Clone the Repository
```bash
git clone https://github.com/ashmijha/Network_Security.git
cd Network_Security
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# On Linux/macOS:
source env/bin/activate

# On Windows:
env\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
# Create .env file from template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

**Required .env variables:**
```bash
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>?retryWrites=true&w=majority
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-1
```

### Step 5: Load Data into MongoDB
```bash
# Run the data push script
python push_data.py

# This will:
# 1. Read Network_Data/phisingData.csv
# 2. Convert CSV to JSON records
# 3. Insert into MongoDB ASHMI_DB.NetworkData collection
```

---

## 🚀 Project Workflow

### Option 1: Direct Python Execution
```bash
# Run the main training pipeline
python main.py

# Or use the modular approach in main.py:
# - Data Ingestion
# - Data Validation
# - Data Transformation
# - Model Training
```

### Option 2: FastAPI Application
```bash
# Start the API server
python app.py

# The server will run at: http://localhost:8000

# Access interactive docs:
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

### Option 3: Using Docker
```bash
# Build the Docker image
docker build -t network-security:latest .

# Run the container
docker run -p 8000:8000 \
  -e MONGODB_URI="your_mongodb_uri" \
  -e AWS_ACCESS_KEY_ID="your_aws_key" \
  -e AWS_SECRET_ACCESS_KEY="your_aws_secret" \
  network-security:latest
```

### Detailed Workflow Steps

#### 1️⃣ Data Ingestion
```python
# Loads data from MongoDB
# File: Network_security/components/data_ingestion.py

DataIngestion:
  ├── export_collection_as_dataframe()
  │   └── Connects to MongoDB and fetches NetworkData
  ├── export_data_into_feature_store()
  │   └── Saves full dataset as CSV
  └── split_data_as_train_test()
      ├── 80% training data
      └── 20% testing data
```

**Output Artifacts:**
- `Artifacts/<timestamp>/data_ingestion/feature_store/phisingData.csv`
- `Artifacts/<timestamp>/data_ingestion/ingested/train.csv`
- `Artifacts/<timestamp>/data_ingestion/ingested/test.csv`

#### 2️⃣ Data Validation
```python
# Validates data quality and detects drift
# File: Network_security/components/data_validation.py

DataValidation:
  ├── validate_number_of_columns()
  │   └── Checks against data_schema/schema.yaml
  └── detect_dataset_drift()
      └── Uses Kolmogorov-Smirnov test (p-value threshold: 0.05)
```

**Output Artifacts:**
- `Artifacts/<timestamp>/data_validation/validated/train.csv`
- `Artifacts/<timestamp>/data_validation/validated/test.csv`
- `Artifacts/<timestamp>/data_validation/drift_report/report.yaml`

#### 3️⃣ Data Transformation
```python
# Transforms features using KNN imputation
# File: Network_security/components/data_transformation.py

DataTransformation:
  ├── get_data_transformer_object()
  │   └── Creates Pipeline with KNNImputer(n_neighbors=3)
  └── initiate_data_transformation()
      ├── Fits preprocessor on training data
      ├── Transforms train features
      ├── Transforms test features
      └── Appends target column
```

**Output Artifacts:**
- `Artifacts/<timestamp>/data_transformation/transformed/train.npy`
- `Artifacts/<timestamp>/data_transformation/transformed/test.npy`
- `Artifacts/<timestamp>/data_transformation/transformed_object/preprocessing.pkl`
- `final_model/preprocessor.pkl` (for inference)

#### 4️⃣ Model Training
```python
# Trains and selects best model
# File: Network_security/components/model_trainer.py

ModelTrainer:
  ├── train_model()
  │   ├── Initialize 5 classifiers
  │   ├── GridSearchCV for hyperparameters
  │   ├── Train and evaluate each model
  │   └── Select best by test score
  ├── track_mlflow()
  │   └── Log metrics: F1, Precision, Recall
  └── initiate_model_trainer()
      └── Create ModelTrainerArtifact
```

**Models Trained:**
| Model | Hyperparameters |
|-------|-----------------|
| Random Forest | n_estimators: [8, 16, 32, 128, 256] |
| Decision Tree | criterion: ['gini', 'entropy', 'log_loss'] |
| Gradient Boosting | learning_rate: [0.1, 0.01, 0.05, 0.001] |
| Logistic Regression | default |
| AdaBoost | n_estimators, learning_rate |

**Output Artifacts:**
- `Artifacts/<timestamp>/model_trainer/trained_model/model.pkl`
- `final_model/model.pkl` (for inference)

---

## 🔌 API Endpoints

### 1. Home / Docs Redirect
```
GET /
```
Redirects to Swagger documentation at `/docs`

### 2. Training Pipeline
```
GET /train
```
**Description**: Triggers the complete training pipeline

**Response**:
```json
{
  "message": "Training is successful"
}
```

**Example**:
```bash
curl -X GET "http://localhost:8000/train"
```

### 3. Prediction
```
POST /predict
```
**Description**: Uploads CSV file and returns predictions

**Parameters**:
- `file` (multipart/form-data): CSV file with features

**Response**: HTML table with predictions

**Example**:
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@input_data.csv"
```

**Input CSV Format**:
```csv
feature1,feature2,feature3,...,featureN
0.5,0.3,0.8,...,0.2
0.6,0.4,0.7,...,0.3
```

---

## 🐳 Docker Setup

### Dockerfile Explanation
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y awscli git

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Install package
RUN pip install -e .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "app.py"]
```

### Build and Run
```bash
# Build image
docker build -t network-security:latest .

# Run container with environment variables
docker run -d \
  --name network-security \
  -p 8000:8000 \
  -e MONGODB_URI="$MONGODB_URI" \
  -e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
  -e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
  network-security:latest

# View logs
docker logs -f network-security

# Stop container
docker stop network-security
```

---

## ⚙️ CI/CD Pipeline

### GitHub Actions Workflow
```yaml
# File: .github/workflows/main.yml
```

**Workflow Steps:**

1. **Trigger**: On push to `main` branch
2. **Checkout**: Clone repository
3. **Setup Python**: Install Python 3.9
4. **Install Dependencies**: `pip install -r requirements.txt`
5. **Linting** (optional): Code quality checks
6. **Run Tests** (optional): Unit tests
7. **Build Docker Image**: Create container
8. **Push to Registry** (optional): Docker Hub or ECR
9. **Deploy** (optional): Deploy to cloud

### Manual GitHub Actions Trigger
```bash
# The workflow runs automatically on:
git push origin main

# Or manually trigger from GitHub UI:
# Actions → Select workflow → Run workflow
```

### Setting Up CI/CD Secrets
In GitHub repository settings, add these secrets:
```
MONGODB_URI              → Your MongoDB connection string
AWS_ACCESS_KEY_ID       → Your AWS access key
AWS_SECRET_ACCESS_KEY   → Your AWS secret key
DOCKER_USERNAME         → Docker Hub username (optional)
DOCKER_PASSWORD         → Docker Hub token (optional)
```

---


---

## 📊 Monitoring & Logging

### Log Files Location
```
logs/
├── MM_DD_YYYY_HH_MM_SS.log
└── (New log created for each run)
```

### View Real-time Logs
```bash
# Follow logs in real-time
tail -f logs/01_01_2025_10_30_45.log

# Search for errors
grep "ERROR" logs/*.log

# View specific component logs
grep "DataTransformation" logs/*.log
```

### MLflow UI
```bash
# Start MLflow UI
mlflow ui --host 0.0.0.0 --port 5000

# Access at: http://localhost:5000
```

---

## 📈 Performance Metrics

### Expected Model Performance
- **F1 Score**: 0.80-0.95 (depending on dataset)
- **Precision**: 0.80-0.90
- **Recall**: 0.75-0.90
- **Training Time**: 2-5 minutes (depends on hardware)

### Data Statistics
- **Total Records**: ~11,000 (phisingData.csv)
- **Features**: 30
- **Target Classes**: Binary (0, 1)
- **Missing Values**: Handled by KNN Imputation

---

---

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **MLflow Documentation**: https://mlflow.org/docs/
- **MongoDB Documentation**: https://docs.mongodb.com/
- **AWS S3 Documentation**: https://docs.aws.amazon.com/s3/
- **scikit-learn Documentation**: https://scikit-learn.org/

---

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see LICENSE file for details.

---


## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

