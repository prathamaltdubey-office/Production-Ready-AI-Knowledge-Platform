const NumberField = ({
  label,
  value,
  onChange,
  min,
  max,
  step = "1",
  hint,
}) => {
  return (
    <div className="form-field">
      <label>
        <span>{label}</span>

        {hint && (
          <small>{hint}</small>
        )}
      </label>

      <input
        type="number"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(event) =>
          onChange(Number(event.target.value))
        }
      />
    </div>
  );
};

export default NumberField;