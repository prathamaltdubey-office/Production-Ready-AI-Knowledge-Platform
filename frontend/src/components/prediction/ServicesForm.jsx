import SelectField from "../form/SelectField";

const yesNo = [
  {
    value: "Yes",
    label: "Yes",
  },
  {
    value: "No",
    label: "No",
  },
];

const internetDependent = [
  {
    value: "Yes",
    label: "Yes",
  },
  {
    value: "No",
    label: "No",
  },
  {
    value: "No internet service",
    label: "No internet service",
  },
];

const ServicesForm = ({
  customer,
  updateCustomer,
}) => {
  return (
    <div className="form-section">
      <div className="form-section-header">
        <div className="section-number">
          02
        </div>

        <div>
          <h3>Services</h3>

          <p>
            Customer subscription details
          </p>
        </div>
      </div>

      <div className="form-grid">
        <SelectField
          label="Phone Service"
          value={customer.PhoneService}
          onChange={(value) =>
            updateCustomer(
              "PhoneService",
              value
            )
          }
          options={yesNo}
        />

        <SelectField
          label="Multiple Lines"
          value={customer.MultipleLines}
          onChange={(value) =>
            updateCustomer(
              "MultipleLines",
              value
            )
          }
          options={[
            {
              value: "Yes",
              label: "Yes",
            },
            {
              value: "No",
              label: "No",
            },
            {
              value: "No phone service",
              label: "No phone service",
            },
          ]}
        />

        <SelectField
          label="Internet Service"
          value={customer.InternetService}
          onChange={(value) =>
            updateCustomer(
              "InternetService",
              value
            )
          }
          options={[
            {
              value: "DSL",
              label: "DSL",
            },
            {
              value: "Fiber optic",
              label: "Fiber optic",
            },
            {
              value: "No",
              label: "No internet",
            },
          ]}
        />

        <SelectField
          label="Online Security"
          value={customer.OnlineSecurity}
          onChange={(value) =>
            updateCustomer(
              "OnlineSecurity",
              value
            )
          }
          options={internetDependent}
        />

        <SelectField
          label="Online Backup"
          value={customer.OnlineBackup}
          onChange={(value) =>
            updateCustomer(
              "OnlineBackup",
              value
            )
          }
          options={internetDependent}
        />

        <SelectField
          label="Device Protection"
          value={customer.DeviceProtection}
          onChange={(value) =>
            updateCustomer(
              "DeviceProtection",
              value
            )
          }
          options={internetDependent}
        />

        <SelectField
          label="Tech Support"
          value={customer.TechSupport}
          onChange={(value) =>
            updateCustomer(
              "TechSupport",
              value
            )
          }
          options={internetDependent}
        />

        <SelectField
          label="Streaming TV"
          value={customer.StreamingTV}
          onChange={(value) =>
            updateCustomer(
              "StreamingTV",
              value
            )
          }
          options={internetDependent}
        />

        <SelectField
          label="Streaming Movies"
          value={customer.StreamingMovies}
          onChange={(value) =>
            updateCustomer(
              "StreamingMovies",
              value
            )
          }
          options={internetDependent}
        />
      </div>
    </div>
  );
};

export default ServicesForm;