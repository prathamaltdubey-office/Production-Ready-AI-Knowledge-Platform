import {
  getProbabilityPercentage,
  clampPercentage,
  getRiskAssessment,
} from "../../utils/predictionUtils";

const RiskDisplay = ({
  prediction,
}) => {
  const probability =
    getProbabilityPercentage(prediction);

  const probabilityPercentage =
    probability ?? 0;

  const barWidth =
    clampPercentage(
      probabilityPercentage
    );

  return (
    <div className="risk-hero">
      <div className="risk-circle">
        <div>
          <strong>
            {probabilityPercentage.toFixed(1)}%
          </strong>

          <span>
            churn probability
          </span>
        </div>
      </div>

      <div className="risk-summary">
        <span className="eyebrow">
          Risk Assessment
        </span>

        <h4>
          {getRiskAssessment(prediction)}
        </h4>

        <div
          className={`risk-badge ${String(
            prediction.risk_level || ""
          ).toLowerCase()}`}
        >
          {prediction.risk_level} Risk
        </div>

        <div className="risk-bar">
          <div
            className="risk-bar-fill"
            style={{
              width: `${barWidth}%`,
            }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default RiskDisplay;