import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { ChevronRight, ChevronLeft } from 'lucide-react';
import { useFormValidation } from './validation/useFormValidation';

const ProducerRegistrationForm = () => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    // Personal Information
    name: '',
    email: '',
    phone: '',
    // Location
    region: 'Galicia',
    city: '',
    address: '',
    // Product Information
    productType: 'honey',
    productName: '',
    quantity: '',
    unit: 'kg',
    // Languages
    languages: {
      galician: true,
      spanish: false,
      english: false
    }
  });

  const { errors, isStepValid } = useFormValidation(formData, step);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    if (type === 'checkbox' && name.startsWith('lang_')) {
      const language = name.replace('lang_', '');
      setFormData(prev => ({
        ...prev,
        languages: {
          ...prev.languages,
          [language]: checked
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const nextStep = () => {
    if (isStepValid) {
      setStep(prev => Math.min(prev + 1, 3));
    }
  };

  const prevStep = () => {
    setStep(prev => Math.max(prev - 1, 1));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!isStepValid) return;

    try {
      // Submit form data to backend
      console.log('Form submitted:', formData);
      // Handle successful submission
    } catch (error) {
      console.error('Submission error:', error);
    }
  };

  // Rest of the component code (form JSX) remains the same as in previous version
};

export default ProducerRegistrationForm;