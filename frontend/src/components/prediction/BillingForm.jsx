import SelectField from "../form/SelectField";
import NumberField from "../form/NumberField";

const BillingForm = ({
  customer,
  updateCustomer,
}) => {
  return (
    <div className="form-section">
      <div className="form-section-header">
        <div className="section-number">
          03
        </div>

        <div>
          <h3>Account & Billing</h3>

          <p>
            Contract and payment information
          </p>
        </div>
      </div>

      <div className="form-grid">
        <SelectField
          label="Contract"
          value={customer.Contract}
          onChange={(value) =>
            updateCustomer(
              "Contract",
              value
            )
          }
          options={[
            {
              value: "Month-to-month",
              label: "Month-to-month",
            },
            {
              value: "One year",
              label: "One year",
            },
            {
              value: "Two year",
              label: "Two year",
            },
          ]}
        />

        <SelectField
          label="Paperless Billing"
          value={customer.PaperlessBilling}
          onChange={(value) =>
            updateCustomer(
              "PaperlessBilling",
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
          ]}
        />

        <SelectField
          label="Payment Method"
          value={customer.PaymentMethod}
          onChange={(value) =>
            updateCustomer(
              "PaymentMethod",
              value
            )
          }
          options={[
            {
              value: "Electronic check",
              label: "Electronic check",
            },
            {
              value: "Mailed check",
              label: "Mailed check",
            },
            {
              value:
                "Bank transfer (automatic)",
              label:
                "Bank transfer (automatic)",
            },
            {
              value:
                "Credit card (automatic)",
              label:
                "Credit card (automatic)",
            },
          ]}
        />

        <NumberField
          label="Monthly Charges"
          hint="Currency"
          value={customer.MonthlyCharges}
          min="0"
          step="0.01"
          onChange={(value) =>
            updateCustomer(
              "MonthlyCharges",
              value
            )
          }
        />

        <NumberField
          label="Total Charges"
          hint="Currency"
          value={customer.TotalCharges}
          min="0"
          step="0.01"
          onChange={(value) =>
            updateCustomer(
              "TotalCharges",
              value
            )
          }
        />
      </div>
    </div>
  );
};

export default BillingForm;