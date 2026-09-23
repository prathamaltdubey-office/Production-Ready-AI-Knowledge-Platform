const SelectField = ({
  label,
  value,
  onChange,
  options,
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

      <select
        value={value}
        onChange={(event) =>
          onChange(event.target.value)
        }
      >
        {options.map((option) => (
          <option
            key={String(option.value)}
            value={option.value}
          >
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default SelectField;