import { useState } from "react";

import { predictCustomer } from "../services/api";
import { defaultCustomer } from "../data/customerDefaults";

const usePrediction = () => {
  const [customer, setCustomer] =
    useState(defaultCustomer);

  const [selectedModel, setSelectedModel] =
    useState("random_forest");

  const [prediction, setPrediction] =
    useState(null);

  const [predictionLoading, setPredictionLoading] =
    useState(false);

  const updateCustomer = (field, value) => {
    setCustomer((previousCustomer) => ({
      ...previousCustomer,
      [field]: value,
    }));

    setPrediction(null);
  };

  const changeModel = (model) => {
    setSelectedModel(model);
    setPrediction(null);
  };

  const runPrediction = async () => {
    setPredictionLoading(true);
    setPrediction(null);

    try {
      const result = await predictCustomer(
        customer,
        selectedModel
      );

      setPrediction(result);
    } catch (error) {
      setPrediction({
        error:
          error.message ||
          "Prediction failed.",
      });
    } finally {
      setPredictionLoading(false);
    }
  };

  return {
    customer,
    selectedModel,
    prediction,
    predictionLoading,
    updateCustomer,
    changeModel,
    runPrediction,
  };
};

export default usePrediction;