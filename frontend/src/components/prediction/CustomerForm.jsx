import CustomerProfile from "./CustomerProfile";
import ServicesForm from "./ServicesForm";
import BillingForm from "./BillingForm";

const CustomerForm = ({
  customer,
  updateCustomer,
}) => {
  return (
    <div className="prediction-form">
      <CustomerProfile
        customer={customer}
        updateCustomer={updateCustomer}
      />

      <ServicesForm
        customer={customer}
        updateCustomer={updateCustomer}
      />

      <BillingForm
        customer={customer}
        updateCustomer={updateCustomer}
      />
    </div>
  );
};

export default CustomerForm;