import SelectField from "../form/SelectField";
import NumberField from "../form/NumberField";

const CustomerProfile = ({
  customer,
  updateCustomer,
}) => {
  return (
    <div className="form-section">
      <div className="form-section-header">
        <div className="section-number">
          01
        </div>

        <div>
          <h3>Customer Profile</h3>

          <p>
            Basic customer information
          </p>
        </div>
      </div>

      <div className="form-grid">
        <SelectField
          label="Gender"
          value={customer.gender}
          onChange={(value) =>
            updateCustomer(
              "gender",
              value
            )
          }
          options={[
            {
              value: "Male",
              label: "Male",
            },
            {
              value: "Female",
              label: "Female",
            },
          ]}
        />

        <SelectField
          label="Senior Citizen"
          value={customer.SeniorCitizen}
          onChange={(value) =>
            updateCustomer(
              "SeniorCitizen",
              Number(value)
            )
          }
          options={[
            {
              value: 0,
              label: "No",
            },
            {
              value: 1,
              label: "Yes",
            },
          ]}
        />

        <SelectField
          label="Partner"
          value={customer.Partner}
          onChange={(value) =>
            updateCustomer(
              "Partner",
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
          label="Dependents"
          value={customer.Dependents}
          onChange={(value) =>
            updateCustomer(
              "Dependents",
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

        <NumberField
          label="Tenure"
          hint="Months"
          value={customer.tenure}
          min="0"
          max="72"
          onChange={(value) =>
            updateCustomer(
              "tenure",
              value
            )
          }
        />
      </div>
    </div>
  );
};

export default CustomerProfile;