import RiskDisplay from "./RiskDisplay";

import {
  getProbabilityPercentage,
  getPredictionLabel,
} from "../../utils/predictionUtils";

const PredictionResult = ({
  prediction,
  selectedModel,
}) => {
  if (!prediction) {
    return null;
  }

  if (prediction.error) {
    return (
      <div className="prediction-result has-error">
        <div className="prediction-error">
          <div className="error-icon">
            !
          </div>

          <div>
            <strong>
              Prediction failed
            </strong>

            <p>
              {prediction.error}
            </p>
          </div>
        </div>
      </div>
    );
  }

  const probability =
    getProbabilityPercentage(prediction);

  const model =
    prediction.model ||
    selectedModel;

  return (
    <div className="prediction-result">
      <div className="result-header">
        <div>
          <span className="eyebrow">
            Prediction Complete
          </span>

          <h3>
            Churn Risk Analysis
          </h3>
        </div>

        <div className="result-model">
          {model}
        </div>
      </div>

      <RiskDisplay
        prediction={prediction}
      />

      <div className="result-grid">
        <div className="result-card">
          <span>
            Prediction
          </span>

          <strong>
            {getPredictionLabel(
              prediction
            )}
          </strong>
        </div>

        <div className="result-card">
          <span>
            Probability
          </span>

          <strong>
            {probability !== null
              ? probability.toFixed(2)
              : "0.00"}
            %
          </strong>
        </div>

        <div className="result-card">
          <span>
            Risk Level
          </span>

          <strong>
            {prediction.risk_level}
          </strong>
        </div>

        <div className="result-card">
          <span>
            Model Used
          </span>

          <strong>
            {model}
          </strong>
        </div>
      </div>
    </div>
  );
};

export default PredictionResult;