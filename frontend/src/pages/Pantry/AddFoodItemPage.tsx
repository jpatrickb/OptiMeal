import { useState, type FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Alert,
  CircularProgress,
  Container,
} from '@mui/material';
import { ArrowBack as ArrowBackIcon, Save as SaveIcon } from '@mui/icons-material';
import NutritionLabelInput from '../../components/NutritionLabelInput';
import type { FoodItemCreate } from '../../types';
import { foodItemsApi } from '../../services/api/foodItems';
import ImageUploadButton from '../../components/ImageUploadButton';

export default function AddFoodItemPage() {
  const navigate = useNavigate();
  const [values, setValues] = useState<Partial<FoodItemCreate>>({});
  const [errors, setErrors] = useState<Partial<Record<keyof FoodItemCreate, string>>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFieldChange = (field: keyof FoodItemCreate, value: any) => {
    setValues({ ...values, [field]: value });
    // Clear error for this field
    if (errors[field]) {
      setErrors({ ...errors, [field]: undefined });
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Partial<Record<keyof FoodItemCreate, string>> = {};

    if (!values.name || values.name.trim() === '') {
      newErrors.name = 'Food name is required';
    }

    if (!values.serving_size || values.serving_size <= 0) {
      newErrors.serving_size = 'Serving size must be greater than 0';
    }

    if (!values.serving_unit || values.serving_unit.trim() === '') {
      newErrors.serving_unit = 'Serving unit is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      await foodItemsApi.create(values as FoodItemCreate);
      navigate('/pantry');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create food item. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ mb: 3 }}>
        <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/pantry')}>
          Back to Pantry
        </Button>
      </Box>

      <Typography variant="h4" component="h1" gutterBottom>
        Add New Food Item
      </Typography>

      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Create a new food item with nutritional information. You can then add it to your pantry.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      <Box component="form" onSubmit={handleSubmit}>
        <Box sx={{ mb: 2 }}>
          <ImageUploadButton
            onFileSelected={async (file) => {
              try {
                const parsed = await foodItemsApi.uploadNutritionLabel(file);
                const updates: Partial<FoodItemCreate> = { ...values };
                if (parsed.calories?.value != null) updates.calories = parsed.calories.value;
                if (parsed.protein_g?.value != null) updates.protein_g = parsed.protein_g.value;
                if (parsed.carbs_g?.value != null) updates.carbs_g = parsed.carbs_g.value;
                if (parsed.fat_g?.value != null) updates.fat_g = parsed.fat_g.value;
                setValues(updates);
              } catch (e: any) {
                setError(e.response?.data?.detail || 'Failed to parse nutrition label');
              }
            }}
          />
        </Box>

        <NutritionLabelInput values={values} onChange={handleFieldChange} errors={errors} />

        <Box sx={{ mt: 3, display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
          <Button variant="outlined" onClick={() => navigate('/pantry')} disabled={loading}>
            Cancel
          </Button>
          <Button
            type="submit"
            variant="contained"
            startIcon={loading ? <CircularProgress size={20} /> : <SaveIcon />}
            disabled={loading}
          >
            {loading ? 'Saving...' : 'Save Food Item'}
          </Button>
        </Box>
      </Box>
    </Container>
  );
}
