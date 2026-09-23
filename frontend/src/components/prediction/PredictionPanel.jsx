import usePrediction from "../../hooks/usePrediction";

import ModelSelector from "./ModelSelector";
import CustomerForm from "./CustomerForm";
import PredictionResult from "./PredictionResult";

const PredictionPanel = () => {
  const {
    customer,
    selectedModel,
    prediction,
    predictionLoading,
    updateCustomer,
    changeModel,
    runPrediction,
  } = usePrediction();

  return (
    <section className="prediction-section glass">
      <div className="panel-header">
        <div className="panel-title-row">
          <div className="panel-icon prediction-icon">
            ◉
          </div>

          <div>
            <h2>
              Churn Prediction
            </h2>

            <p>
              Analyze customer information and
              estimate churn risk.
            </p>
          </div>
        </div>

        <div className="model-count">
          <strong>3</strong>
          Models
        </div>
      </div>

      <ModelSelector
        selectedModel={selectedModel}
        onModelChange={changeModel}
      />

      <CustomerForm
        customer={customer}
        updateCustomer={updateCustomer}
      />

      <div className="prediction-action">
        <button
          className="predict-button"
          onClick={runPrediction}
          disabled={predictionLoading}
        >
          {predictionLoading ? (
            <>
              <span className="button-spinner"></span>
              Analyzing customer...
            </>
          ) : (
            <>
              <span className="predict-icon">
                ◈
              </span>

              Predict Churn Risk
            </>
          )}
        </button>

        <p>
          The selected ML model will analyze
          the customer profile and calculate
          churn probability.
        </p>
      </div>

      <PredictionResult
        prediction={prediction}
        selectedModel={selectedModel}
      />
    </section>
  );
};

export default PredictionPanel;