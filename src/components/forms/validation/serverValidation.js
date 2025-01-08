// Server-side validation types
export const ValidationTypes = {
  REQUIRED: 'required',
  MIN_LENGTH: 'minLength',
  PATTERN: 'pattern',
  CUSTOM: 'custom'
};

// Server-side validation schema
export const serverValidationSchema = {
  name: [
    { type: ValidationTypes.REQUIRED, message: 'Name is required' },
    { type: ValidationTypes.MIN_LENGTH, value: 2, message: 'Name must be at least 2 characters' },
    { type: ValidationTypes.PATTERN, value: /^[a-zA-ZÀ-ÿ\s']+$/, message: 'Name can only contain letters and spaces' }
  ],
  email: [
    { type: ValidationTypes.REQUIRED, message: 'Email is required' },
    { type: ValidationTypes.PATTERN, value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, message: 'Invalid email format' }
  ],
  phone: [
    { type: ValidationTypes.REQUIRED, message: 'Phone number is required' },
    { type: ValidationTypes.PATTERN, value: /^\+?\d{9,15}$/, message: 'Invalid phone number format' }
  ],
  // Add other field validations
};

// Server-side validation function
export const validateFormData = (data) => {
  const errors = {};
  
  Object.entries(serverValidationSchema).forEach(([field, rules]) => {
    const value = data[field];
    
    rules.forEach(rule => {
      switch (rule.type) {
        case ValidationTypes.REQUIRED:
          if (!value) errors[field] = rule.message;
          break;
        case ValidationTypes.MIN_LENGTH:
          if (value.length < rule.value) errors[field] = rule.message;
          break;
        case ValidationTypes.PATTERN:
          if (!rule.value.test(value)) errors[field] = rule.message;
          break;
        case ValidationTypes.CUSTOM:
          if (!rule.validate(value)) errors[field] = rule.message;
          break;
      }
    });
  });
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};
