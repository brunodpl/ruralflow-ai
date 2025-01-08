import { useState, useEffect } from 'react';

export const useFormValidation = (formData, step) => {
  const [errors, setErrors] = useState({});
  const [isStepValid, setIsStepValid] = useState(false);

  // Validation rules
  const rules = {
    // Step 1: Personal Information
    name: {
      required: true,
      minLength: 2,
      pattern: /^[a-zA-ZÀ-ÿ\s']+$/,
      message: {
        required: 'Name is required',
        minLength: 'Name must be at least 2 characters',
        pattern: 'Name can only contain letters and spaces'
      }
    },
    email: {
      required: true,
      pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
      message: {
        required: 'Email is required',
        pattern: 'Please enter a valid email address'
      }
    },
    phone: {
      required: true,
      pattern: /^\+?\d{9,15}$/,
      message: {
        required: 'Phone number is required',
        pattern: 'Please enter a valid phone number'
      }
    },
    languages: {
      required: true,
      validate: (value) => Object.values(value).some(v => v),
      message: {
        required: 'Please select at least one language'
      }
    },

    // Step 2: Location
    region: {
      required: true,
      message: {
        required: 'Region is required'
      }
    },
    city: {
      required: true,
      minLength: 2,
      message: {
        required: 'City is required',
        minLength: 'City name must be at least 2 characters'
      }
    },
    address: {
      required: true,
      minLength: 5,
      message: {
        required: 'Address is required',
        minLength: 'Address must be at least 5 characters'
      }
    },

    // Step 3: Product Information
    productType: {
      required: true,
      message: {
        required: 'Product type is required'
      }
    },
    productName: {
      required: true,
      minLength: 3,
      message: {
        required: 'Product name is required',
        minLength: 'Product name must be at least 3 characters'
      }
    },
    quantity: {
      required: true,
      validate: (value) => !isNaN(value) && parseFloat(value) > 0,
      message: {
        required: 'Quantity is required',
        validate: 'Quantity must be a positive number'
      }
    }
  };

  // Validation logic implementation
  const validateField = (name, value) => {
    const rule = rules[name];
    if (!rule) return null;

    if (rule.required && (!value || (typeof value === 'string' && !value.trim()))) {
      return rule.message.required;
    }

    if (rule.minLength && value.length < rule.minLength) {
      return rule.message.minLength;
    }

    if (rule.pattern && !rule.pattern.test(value)) {
      return rule.message.pattern;
    }

    if (rule.validate && !rule.validate(value)) {
      return rule.message.validate;
    }

    return null;
  };

  const validateStep = () => {
    const newErrors = {};
    
    const stepFields = {
      1: ['name', 'email', 'phone', 'languages'],
      2: ['region', 'city', 'address'],
      3: ['productType', 'productName', 'quantity']
    };

    stepFields[step].forEach(field => {
      const error = validateField(field, formData[field]);
      if (error) {
        newErrors[field] = error;
      }
    });

    setErrors(newErrors);
    setIsStepValid(Object.keys(newErrors).length === 0);
  };

  useEffect(() => {
    validateStep();
  }, [formData, step]);

  return { errors, isStepValid };
};
