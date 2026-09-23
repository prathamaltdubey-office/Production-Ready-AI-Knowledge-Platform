from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd

from src.evaluate import clean_data as eval_clean_data
from src.evaluate import (
    evaluate_models,
)
from src.evaluate import load_data as eval_load_data
from src.evaluate import (
    load_models,
    save_metrics,
)
from src.evaluate import split_data as eval_split_data
from src.train import (
    clean_data,
    create_preprocessor,
    load_data,
    main,
    split_data,
    train_models,
)
from src.tuning import clean_data as tuning_clean_data
from src.tuning import (
    create_logistic_pipeline,
)
from src.tuning import create_preprocessor as tuning_create_preprocessor
from src.tuning import (
    create_rf_pipeline,
    create_xgb_pipeline,
)
from src.tuning import load_data as tuning_load_data
from src.tuning import (
    logistic_params,
    rf_params,
)
from src.tuning import split_data as tuning_split_data
from src.tuning import (
    xgb_params,
)


def sample_dataframe() -> pd.DataFrame:
    """
    Create a sample dataset for testing.
    """

    df = pd.DataFrame(
        {
            "customerID": ["1", "2", "3"],
            "gender": ["Male", "Female", "Male"],
            "SeniorCitizen": [0, 1, 0],
            "Partner": ["Yes", "No", "Yes"],
            "Dependents": ["No", "Yes", "No"],
            "tenure": [12, 24, 36],
            "PhoneService": ["Yes", "Yes", "No"],
            "MultipleLines": [
                "No",
                "Yes",
                "No phone service",
            ],
            "InternetService": [
                "DSL",
                "Fiber optic",
                "No",
            ],
            "OnlineSecurity": [
                "Yes",
                "No",
                "No internet service",
            ],
            "OnlineBackup": [
                "No",
                "Yes",
                "No internet service",
            ],
            "DeviceProtection": [
                "Yes",
                "No",
                "No internet service",
            ],
            "TechSupport": [
                "No",
                "Yes",
                "No internet service",
            ],
            "StreamingTV": [
                "No",
                "Yes",
                "No internet service",
            ],
            "StreamingMovies": [
                "No",
                "Yes",
                "No internet service",
            ],
            "Contract": [
                "Month-to-month",
                "One year",
                "Two year",
            ],
            "PaperlessBilling": [
                "Yes",
                "No",
                "Yes",
            ],
            "PaymentMethod": [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
            ],
            "MonthlyCharges": [
                70.35,
                89.10,
                25.20,
            ],
            "TotalCharges": [
                "843.2",
                "2138.4",
                "907.2",
            ],
            "Churn": [
                "Yes",
                "No",
                "No",
            ],
        }
    )

    # Duplicate rows to create a larger dataset
    df = pd.concat([df] * 4, ignore_index=True)

    return df


def test_clean_data():
    """
    Test dataset cleaning.
    """

    df = sample_dataframe()

    cleaned = clean_data(df)

    assert "customerID" not in cleaned.columns

    assert cleaned["Churn"].isin([0, 1]).all()

    assert cleaned["TotalCharges"].dtype == "float64"


def test_split_data():
    """
    Test train-test split.
    """

    df = clean_data(sample_dataframe())

    X_train, X_test, y_train, y_test = split_data(df)

    assert len(X_train) > 0
    assert len(X_test) > 0
    assert len(y_train) > 0
    assert len(y_test) > 0


def test_create_preprocessor():
    """
    Test preprocessing pipeline creation.
    """

    df = clean_data(sample_dataframe())

    X_train, _, _, _ = split_data(df)

    preprocessor = create_preprocessor(X_train)

    assert preprocessor is not None

    assert hasattr(preprocessor, "fit")

    assert hasattr(preprocessor, "transform")


def test_load_data():
    """
    Test dataset loading.
    """

    df = load_data()

    assert not df.empty

    assert "customerID" in df.columns

    assert "Churn" in df.columns


def test_train_models():
    """
    Test model training.
    """

    df = clean_data(load_data())

    X_train, _, y_train, _ = split_data(df)

    preprocessor = create_preprocessor(X_train)

    train_models(
        X_train,
        y_train,
        preprocessor,
    )

    assert Path("models/logistic_model.pkl").exists()

    assert Path("models/rf_model.pkl").exists()

    assert Path("models/xgb_model.pkl").exists()


def test_main():
    """
    Test complete training workflow.
    """

    main()

    assert Path("models/logistic_model.pkl").exists()

    assert Path("models/rf_model.pkl").exists()

    assert Path("models/xgb_model.pkl").exists()


def test_evaluate_load_data():
    """
    Test loading dataset for evaluation.
    """

    df = eval_load_data()

    assert not df.empty

    assert "customerID" in df.columns

    assert "Churn" in df.columns


def test_evaluate_clean_data():
    """
    Test cleaning dataset.
    """

    df = sample_dataframe()

    cleaned = eval_clean_data(df)

    assert "customerID" not in cleaned.columns

    assert cleaned["Churn"].isin([0, 1]).all()

    assert cleaned["TotalCharges"].dtype == "float64"


def test_evaluate_split_data():
    """
    Test train-test split.
    """

    df = eval_clean_data(sample_dataframe())

    X_train, X_test, y_train, y_test = eval_split_data(df)

    assert len(X_train) > 0

    assert len(X_test) > 0

    assert len(y_train) > 0

    assert len(y_test) > 0


def test_load_models():
    """
    Test loading trained models.
    """

    models = load_models()

    assert len(models) == 3

    assert "Tuned Logistic Regression" in models

    assert "Tuned Random Forest" in models

    assert "Tuned XGBoost" in models


def test_evaluate_models():
    """
    Test model evaluation.
    """

    df = eval_clean_data(eval_load_data())

    _, X_test, _, y_test = eval_split_data(df)

    models = load_models()

    metrics = evaluate_models(
        models,
        X_test,
        y_test,
    )

    assert not metrics.empty

    assert len(metrics) == 3

    assert "Accuracy" in metrics.columns

    assert "Precision" in metrics.columns

    assert "Recall" in metrics.columns

    assert "F1 Score" in metrics.columns

    assert "ROC-AUC" in metrics.columns


def test_save_metrics():
    """
    Test saving evaluation metrics.
    """

    metrics = pd.DataFrame(
        {
            "Model": ["Test Model"],
            "Accuracy": [0.90],
            "Precision": [0.91],
            "Recall": [0.92],
            "F1 Score": [0.91],
            "ROC-AUC": [0.95],
        }
    )

    save_metrics(metrics)

    assert Path("reports/model_metrics.csv").exists()


def test_tuning_load_data():
    """
    Test dataset loading for tuning.
    """

    df = tuning_load_data()

    assert not df.empty

    assert "customerID" in df.columns

    assert "Churn" in df.columns


def test_tuning_clean_data():
    """
    Test dataset cleaning.
    """

    df = sample_dataframe()

    cleaned = tuning_clean_data(df)

    assert "customerID" not in cleaned.columns

    assert cleaned["Churn"].isin([0, 1]).all()

    assert cleaned["TotalCharges"].dtype == "float64"


def test_tuning_split_data():
    """
    Test train-test split.
    """

    df = tuning_clean_data(load_data())

    X_train, X_test, y_train, y_test = tuning_split_data(df)

    assert len(X_train) > 0

    assert len(X_test) > 0

    assert len(y_train) > 0

    assert len(y_test) > 0


def test_tuning_create_preprocessor():
    """
    Test preprocessing pipeline creation.
    """

    df = tuning_clean_data(load_data())

    X_train, _, _, _ = tuning_split_data(df)

    preprocessor = tuning_create_preprocessor(X_train)

    assert preprocessor is not None

    assert hasattr(preprocessor, "fit")

    assert hasattr(preprocessor, "transform")


def test_logistic_params():
    """
    Test Logistic Regression parameter grid.
    """

    params = logistic_params()

    assert isinstance(params, dict)

    assert "model__C" in params

    assert "model__solver" in params

    assert "model__penalty" in params


def test_rf_params():
    """
    Test Random Forest parameter grid.
    """

    params = rf_params()

    assert isinstance(params, dict)

    assert "model__n_estimators" in params

    assert "model__max_depth" in params


def test_xgb_params():
    """
    Test XGBoost parameter grid.
    """

    params = xgb_params()

    assert isinstance(params, dict)

    assert "model__learning_rate" in params

    assert "model__n_estimators" in params


def test_create_logistic_pipeline():
    """
    Test Logistic Regression pipeline creation.
    """

    df = tuning_clean_data(load_data())

    X_train, _, y_train, _ = tuning_split_data(df)

    preprocessor = tuning_create_preprocessor(X_train)

    pipeline = create_logistic_pipeline(preprocessor)

    assert pipeline is not None

    assert hasattr(pipeline, "fit")


def test_create_rf_pipeline():
    """
    Test Random Forest pipeline creation.
    """

    df = tuning_clean_data(load_data())

    X_train, _, y_train, _ = tuning_split_data(df)

    preprocessor = tuning_create_preprocessor(X_train)

    pipeline = create_rf_pipeline(preprocessor)

    assert pipeline is not None

    assert hasattr(pipeline, "fit")


def test_create_xgb_pipeline():
    """
    Test XGBoost pipeline creation.
    """

    df = tuning_clean_data(load_data())

    X_train, _, y_train, _ = tuning_split_data(df)

    preprocessor = tuning_create_preprocessor(X_train)

    pipeline = create_xgb_pipeline(preprocessor)

    assert pipeline is not None

    assert hasattr(pipeline, "fit")


def test_tune_logistic():
    """
    Test Logistic Regression tuning without actually training.
    """

    from src.tuning import tune_logistic

    df = tuning_clean_data(tuning_load_data())

    X_train, _, y_train, _ = tuning_split_data(df)

    preprocessor = tuning_create_preprocessor(X_train)

    fake_search = MagicMock()

    fake_search.best_params_ = {"model__C": 1}

    fake_search.best_score_ = 0.91

    fake_search.best_estimator_ = MagicMock()

    with (
        patch("src.tuning.RandomizedSearchCV", return_value=fake_search),
        patch("src.tuning.mlflow.start_run"),
        patch("src.tuning.mlflow.log_params"),
        patch("src.tuning.mlflow.log_metric"),
        patch("src.tuning.mlflow.sklearn.log_model"),
        patch("src.tuning.dump"),
        patch("src.tuning.register_model"),
    ):
        tune_logistic(
            X_train,
            y_train,
            preprocessor,
        )

    fake_search.fit.assert_called_once()


def test_tune_random_forest():
    """
    Test Random Forest tuning without actually training.
    """

    from src.tuning import tune_random_forest

    df = tuning_clean_data(tuning_load_data())

    X_train, _, y_train, _ = tuning_split_data(df)

    preprocessor = tuning_create_preprocessor(X_train)

    fake_search = MagicMock()

    fake_search.best_params_ = {"model__n_estimators": 100}

    fake_search.best_score_ = 0.94

    fake_search.best_estimator_ = MagicMock()

    with (
        patch("src.tuning.RandomizedSearchCV", return_value=fake_search),
        patch("src.tuning.mlflow.start_run"),
        patch("src.tuning.mlflow.log_params"),
        patch("src.tuning.mlflow.log_metric"),
        patch("src.tuning.mlflow.sklearn.log_model"),
        patch("src.tuning.dump"),
        patch("src.tuning.register_model"),
    ):
        tune_random_forest(
            X_train,
            y_train,
            preprocessor,
        )

    fake_search.fit.assert_called_once()


def test_tune_xgboost():
    """
    Test XGBoost tuning without actually training.
    """

    from src.tuning import tune_xgboost

    df = tuning_clean_data(tuning_load_data())

    X_train, _, y_train, _ = tuning_split_data(df)

    preprocessor = tuning_create_preprocessor(X_train)

    fake_search = MagicMock()

    fake_search.best_params_ = {
        "model__learning_rate": 0.1,
    }

    fake_search.best_score_ = 0.95

    fake_search.best_estimator_ = MagicMock()

    with (
        patch("src.tuning.RandomizedSearchCV", return_value=fake_search),
        patch("src.tuning.mlflow.start_run"),
        patch("src.tuning.mlflow.log_params"),
        patch("src.tuning.mlflow.log_metric"),
        patch("src.tuning.mlflow.sklearn.log_model"),
        patch("src.tuning.dump"),
        patch("src.tuning.register_model"),
    ):
        tune_xgboost(
            X_train,
            y_train,
            preprocessor,
        )

    fake_search.fit.assert_called_once()
