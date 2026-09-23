const models = [
  {
    value: "logistic_regression",
    shortName: "LR",
    name: "Logistic Regression",
    description: "Linear classification",
  },
  {
    value: "random_forest",
    shortName: "RF",
    name: "Random Forest",
    description: "Ensemble learning",
  },
  {
    value: "xgboost",
    shortName: "XG",
    name: "XGBoost",
    description: "Gradient boosting",
  },
];

const ModelSelector = ({
  selectedModel,
  onModelChange,
}) => {
  return (
    <div className="model-selector-wrapper">
      <div className="model-selector-heading">
        <div>
          <span className="eyebrow">
            Prediction Engine
          </span>

          <h3>
            Select your ML model
          </h3>
        </div>

        <span className="model-badge">
          ML
        </span>
      </div>

      <div className="model-options">
        {models.map((model) => (
          <button
            key={model.value}
            type="button"
            className={`model-option ${
              selectedModel === model.value
                ? "active"
                : ""
            }`}
            onClick={() =>
              onModelChange(model.value)
            }
          >
            <span className="model-option-icon">
              {model.shortName}
            </span>

            <span>
              <strong>
                {model.name}
              </strong>

              <small>
                {model.description}
              </small>
            </span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default ModelSelector;