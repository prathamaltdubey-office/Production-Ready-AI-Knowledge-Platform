"""
Perform hyperparameter tuning for customer churn prediction models.

This script loads the dataset, preprocesses the data,
performs hyperparameter tuning for multiple machine
learning models using RandomizedSearchCV, logs the
results with MLflow, registers each version in the model
registry, and saves the best models.
"""

import mlflow
import pandas as pd
from joblib import dump
from mlflow import sklearn
from mlflow.sklearn import SERIALIZATION_FORMAT_CLOUDPICKLE
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (
    RandomizedSearchCV,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
)
from xgboost import XGBClassifier

from src.model_registry import register_model

mlflow.set_experiment("Customer Churn Prediction")


def load_data() -> pd.DataFrame:
    """
    Load the Telco Customer Churn dataset.

    Returns:
        pd.DataFrame: Loaded dataset.
    """

    return pd.read_csv("./data/Telco_Customer_churn.csv")


def clean_data(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Clean and preprocess the dataset.

    Args:
        df: Raw customer churn dataset.

    Returns:
        pd.DataFrame: Cleaned dataset.
    """

    df = df.drop(
        "customerID",
        axis=1,
    )

    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"],
        errors="coerce",
    )

    df["TotalCharges"] = df["TotalCharges"].fillna(0)

    df["Churn"] = df["Churn"].map(
        {
            "Yes": 1,
            "No": 0,
        }
    )

    return df


def split_data(
    df: pd.DataFrame,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.Series,
    pd.Series,
]:
    """
    Split dataset into train and test sets.
    """

    X = df.drop(
        "Churn",
        axis=1,
    )

    y = df["Churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    return X_train, X_test, y_train, y_test


def create_preprocessor(
    X_train: pd.DataFrame,
) -> ColumnTransformer:
    """
    Create preprocessing pipeline.
    """

    categorical_columns = X_train.select_dtypes(include="object").columns

    numerical_columns = X_train.select_dtypes(exclude="object").columns

    return ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(
                    handle_unknown="ignore",
                ),
                categorical_columns,
            ),
            (
                "num",
                StandardScaler(),
                numerical_columns,
            ),
        ]
    )


def create_logistic_pipeline(
    preprocessor: ColumnTransformer,
) -> Pipeline:
    """
    Create Logistic Regression pipeline.
    """

    return Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "model",
                LogisticRegression(
                    random_state=42,
                    max_iter=1000,
                ),
            ),
        ]
    )


def logistic_params() -> dict:
    """
    Logistic Regression parameter grid.
    """

    return {
        "model__C": [
            0.001,
            0.01,
            0.1,
            1,
            10,
            100,
        ],
        "model__solver": [
            "liblinear",
            "lbfgs",
        ],
        "model__penalty": [
            "l2",
        ],
    }


def create_rf_pipeline(
    preprocessor: ColumnTransformer,
) -> Pipeline:
    """
    Create Random Forest pipeline.
    """

    return Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "model",
                RandomForestClassifier(
                    random_state=42,
                ),
            ),
        ]
    )


def rf_params() -> dict:
    """
    Random Forest parameter grid.
    """

    return {
        "model__n_estimators": [
            100,
            200,
            300,
        ],
        "model__max_depth": [
            5,
            10,
            20,
            None,
        ],
        "model__min_samples_split": [
            2,
            5,
            10,
        ],
        "model__min_samples_leaf": [
            1,
            2,
            4,
        ],
    }


def create_xgb_pipeline(
    preprocessor: ColumnTransformer,
) -> Pipeline:
    """
    Create XGBoost pipeline.
    """

    return Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "model",
                XGBClassifier(
                    random_state=42,
                ),
            ),
        ]
    )


def xgb_params() -> dict:
    """
    XGBoost parameter grid.
    """

    return {
        "model__n_estimators": [
            100,
            200,
            300,
        ],
        "model__learning_rate": [
            0.01,
            0.05,
            0.1,
        ],
        "model__max_depth": [
            3,
            5,
            7,
        ],
        "model__subsample": [
            0.7,
            0.8,
            1.0,
        ],
    }


def tune_logistic(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    preprocessor: ColumnTransformer,
) -> None:
    """
    Tune Logistic Regression model.

    Args:
        X_train: Training features.
        y_train: Training labels.
        preprocessor: Preprocessing pipeline.
    """

    pipeline = create_logistic_pipeline(preprocessor)

    params = logistic_params()

    search = RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=params,
        n_iter=10,
        cv=5,
        scoring="roc_auc",
        random_state=42,
        n_jobs=-1,
    )

    with mlflow.start_run(
        run_name="Logistic Regression",
    ) as run:

        search.fit(
            X_train,
            y_train,
        )

        print("Best Logistic Regression Parameters:")

        print(search.best_params_)

        mlflow.log_params(search.best_params_)

        mlflow.log_metric(
            "best_cv_score",
            search.best_score_,
        )

        sklearn.log_model(
            sk_model=search.best_estimator_,
            name="model",
            serialization_format=SERIALIZATION_FORMAT_CLOUDPICKLE,
        )

        model_path = "models/best_logistic_model.pkl"

        dump(
            search.best_estimator_,
            model_path,
        )

        version = register_model(
            model_name="logistic_regression",
            file_path=model_path,
            metrics={"best_cv_score": search.best_score_},
            mlflow_run_id=run.info.run_id,
            params=search.best_params_,
        )

        print(f"Logistic Regression model saved as version {version}.\n")


def tune_random_forest(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    preprocessor: ColumnTransformer,
) -> None:
    """
    Tune Random Forest model.

    Args:
        X_train: Training features.
        y_train: Training labels.
        preprocessor: Preprocessing pipeline.
    """

    pipeline = create_rf_pipeline(preprocessor)

    params = rf_params()

    search = RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=params,
        n_iter=10,
        cv=5,
        scoring="roc_auc",
        random_state=42,
        n_jobs=-1,
    )

    with mlflow.start_run(
        run_name="Random Forest",
    ) as run:

        search.fit(
            X_train,
            y_train,
        )

        print("Best Random Forest Parameters:")

        print(search.best_params_)

        mlflow.log_params(search.best_params_)

        mlflow.log_metric(
            "best_cv_score",
            search.best_score_,
        )

        sklearn.log_model(
            sk_model=search.best_estimator_,
            name="model",
            serialization_format=SERIALIZATION_FORMAT_CLOUDPICKLE,
        )

        model_path = "models/best_rf_model.pkl"

        dump(
            search.best_estimator_,
            model_path,
        )

        version = register_model(
            model_name="random_forest",
            file_path=model_path,
            metrics={"best_cv_score": search.best_score_},
            mlflow_run_id=run.info.run_id,
            params=search.best_params_,
        )

        print(f"Random Forest model saved as version {version}.\n")


def tune_xgboost(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    preprocessor: ColumnTransformer,
) -> None:
    """
    Tune XGBoost model.

    Args:
        X_train: Training features.
        y_train: Training labels.
        preprocessor: Preprocessing pipeline.
    """

    pipeline = create_xgb_pipeline(preprocessor)

    params = xgb_params()

    search = RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=params,
        n_iter=10,
        cv=5,
        scoring="roc_auc",
        random_state=42,
        n_jobs=-1,
    )

    with mlflow.start_run(
        run_name="XGBoost",
    ) as run:

        search.fit(
            X_train,
            y_train,
        )

        print("Best XGBoost Parameters:")

        print(search.best_params_)

        mlflow.log_params(search.best_params_)

        mlflow.log_metric(
            "best_cv_score",
            search.best_score_,
        )

        sklearn.log_model(
            sk_model=search.best_estimator_,
            name="model",
            serialization_format=SERIALIZATION_FORMAT_CLOUDPICKLE,
        )

        model_path = "models/best_xgb_model.pkl"

        dump(
            search.best_estimator_,
            model_path,
        )

        version = register_model(
            model_name="xgboost",
            file_path=model_path,
            metrics={"best_cv_score": search.best_score_},
            mlflow_run_id=run.info.run_id,
            params=search.best_params_,
        )

        print(f"XGBoost model saved as version {version}.\n")


def main() -> None:
    """
    Execute the complete hyperparameter tuning workflow.
    """

    df = load_data()

    df = clean_data(df)

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = split_data(df)

    preprocessor = create_preprocessor(X_train)

    tune_logistic(
        X_train,
        y_train,
        preprocessor,
    )

    tune_random_forest(
        X_train,
        y_train,
        preprocessor,
    )

    tune_xgboost(
        X_train,
        y_train,
        preprocessor,
    )

    print("\nHyperparameter tuning completed successfully!")


if __name__ == "__main__":
    main()
