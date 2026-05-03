# Task 5: Machine Learning Pipeline with Feature Engineering

A machine learning project to predict customer churn using the **Telco Customer Churn** dataset. It follows a complete end-to-end pipeline from data ingestion to model deployment.

---

## Features

- **Data Preprocessing**
  - Handles hidden missing values in `TotalCharges`.
  - Drops non-predictive columns like `customerID`.
  
- **Feature Engineering**
  - Bins `tenure` into 'new', 'mid', and 'loyal' categories.
  - Calculates `avg_monthly_spend` as a derived feature.

- **Automated Encoding**
  - Uses One-hot encoding for all categorical variables.
  - Ensures all columns are numeric for model compatibility.

- **Model Selection & Tuning**
  - Compares **Logistic Regression**, **Random Forest**, **XGBoost**, and **SVM**.
  - Uses **GridSearchCV** for hyperparameter tuning of the best model.
  - Implements 5-Fold Cross-Validation for robust performance estimation.

- **Insights & Deployment**
  - Extracts **Feature Importances** (Coefficients) to understand churn drivers.
  - Saves the final trained model to the `models/` directory for production use.

---

## Tech Stack

- **Python 3**
- **Pandas** & **NumPy**
- **Scikit-learn**
- **XGBoost**
- **Joblib** (for model saving)
- **Jupyter Notebook**

---

## Project Workflow

1. **Data Acquisition**: Fetch the dataset from a remote IBM raw URL.
2. **Data Cleaning**: Fix data types and fill missing values using the median.
3. **Feature Engineering**: Create new features and encode categorical data.
4. **Model Selection**: Run cross-validation across multiple baseline models.
5. **Hyperparameter Tuning**: Optimize the best model (Logistic Regression) using Grid Search.
6. **Final Evaluation**: Test the tuned model on the held-out test set (Metrics: Accuracy, F1, ROC-AUC).
7. **Feature Importance**: Analyze coefficients to identify top predictors of churn.
8. **Serialization**: Save the final model as `models/churn_lr_model.pkl`.

---

## Model Evaluation

- **Primary Metric**: **F1-score** (to handle the class imbalance between churned and retained customers).
- **Secondary Metrics**: Accuracy, Precision, Recall, and ROC-AUC.
- **Handling Imbalance**: Uses `class_weight='balanced'` to ensure the model doesn't ignore the minority (churn) class.

---

## Installation

```bash
pip install pandas numpy scikit-learn xgboost joblib notebook
jupyter notebook model.ipynb
```
