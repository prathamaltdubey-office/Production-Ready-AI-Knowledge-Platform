export const getProbabilityPercentage = (
  prediction
) => {
  if (
    !prediction ||
    prediction.error ||
    typeof prediction.churn_probability !==
      "number"
  ) {
    return null;
  }

  return prediction.churn_probability * 100;
};

export const clampPercentage = (value) => {
  return Math.min(
    100,
    Math.max(0, value)
  );
};

export const getPredictionLabel = (
  prediction
) => {
  return prediction?.prediction === 1
    ? "Will Churn"
    : "Will Stay";
};

export const getRiskAssessment = (
  prediction
) => {
  return prediction?.prediction === 1
    ? "Likely to Churn"
    : "Unlikely to Churn";
};