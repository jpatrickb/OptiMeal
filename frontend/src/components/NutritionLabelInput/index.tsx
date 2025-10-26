import { Box, TextField, Typography, Grid, Divider, Paper } from '@mui/material';
import type { FoodItemCreate } from '../../types';

interface NutritionLabelInputProps {
  values: Partial<FoodItemCreate>;
  onChange: (field: keyof FoodItemCreate, value: any) => void;
  errors?: Partial<Record<keyof FoodItemCreate, string>>;
}

export default function NutritionLabelInput({ values, onChange, errors }: NutritionLabelInputProps) {
  const handleNumberChange = (field: keyof FoodItemCreate, value: string) => {
    const numValue = value === '' ? undefined : parseFloat(value);
    onChange(field, numValue);
  };

  return (
    <Paper elevation={2} sx={{ p: 3, mt: 2 }}>
      <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', textAlign: 'center' }}>
        Nutrition Facts
      </Typography>

      {/* Basic Info */}
      <Box sx={{ mb: 3 }}>
        <TextField
          fullWidth
          required
          label="Food Name"
          value={values.name || ''}
          onChange={(e) => onChange('name', e.target.value)}
          error={!!errors?.name}
          helperText={errors?.name}
          margin="normal"
        />
        <TextField
          fullWidth
          label="Brand (optional)"
          value={values.brand || ''}
          onChange={(e) => onChange('brand', e.target.value)}
          margin="normal"
        />
      </Box>

      <Divider sx={{ my: 2 }} />

      {/* Serving Size */}
      <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 'bold' }}>
        Serving Information
      </Typography>
      <Grid container spacing={2}>
        <Grid size={{ xs: 6 }}>
          <TextField
            fullWidth
            required
            type="number"
            label="Serving Size"
            value={values.serving_size || ''}
            onChange={(e) => handleNumberChange('serving_size', e.target.value)}
            error={!!errors?.serving_size}
            helperText={errors?.serving_size}
            inputProps={{ min: 0, step: 0.1 }}
          />
        </Grid>
        <Grid size={{ xs: 6 }}>
          <TextField
            fullWidth
            required
            label="Unit"
            placeholder="cup, oz, g, etc."
            value={values.serving_unit || ''}
            onChange={(e) => onChange('serving_unit', e.target.value)}
            error={!!errors?.serving_unit}
            helperText={errors?.serving_unit}
          />
        </Grid>
      </Grid>

      <Divider sx={{ my: 2 }} />

      {/* Macronutrients */}
      <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 'bold' }}>
        Macronutrients (per serving)
      </Typography>
      <Grid container spacing={2}>
        <Grid size={{ xs: 6 }}>
          <TextField
            fullWidth
            type="number"
            label="Calories"
            value={values.calories || ''}
            onChange={(e) => handleNumberChange('calories', e.target.value)}
            inputProps={{ min: 0 }}
          />
        </Grid>
        <Grid size={{ xs: 6 }}>
          <TextField
            fullWidth
            type="number"
            label="Protein (g)"
            value={values.protein_g || ''}
            onChange={(e) => handleNumberChange('protein_g', e.target.value)}
            inputProps={{ min: 0, step: 0.1 }}
          />
        </Grid>
        <Grid size={{ xs: 6 }}>
          <TextField
            fullWidth
            type="number"
            label="Carbohydrates (g)"
            value={values.carbs_g || ''}
            onChange={(e) => handleNumberChange('carbs_g', e.target.value)}
            inputProps={{ min: 0, step: 0.1 }}
          />
        </Grid>
        <Grid size={{ xs: 6 }}>
          <TextField
            fullWidth
            type="number"
            label="Total Fat (g)"
            value={values.fat_g || ''}
            onChange={(e) => handleNumberChange('fat_g', e.target.value)}
            inputProps={{ min: 0, step: 0.1 }}
          />
        </Grid>
      </Grid>

      <Divider sx={{ my: 2 }} />

      {/* Fat Breakdown */}
      <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 'bold' }}>
        Fat Breakdown
      </Typography>
      <Grid container spacing={2}>
        <Grid size={{ xs: 4 }}>
          <TextField
            fullWidth
            type="number"
            label="Saturated Fat (g)"
            value={values.saturated_fat_g || ''}
            onChange={(e) => handleNumberChange('saturated_fat_g', e.target.value)}
            inputProps={{ min: 0, step: 0.1 }}
          />
        </Grid>
        <Grid size={{ xs: 4 }}>
          <TextField
            fullWidth
            type="number"
            label="Trans Fat (g)"
            value={values.trans_fat_g || ''}
            onChange={(e) => handleNumberChange('trans_fat_g', e.target.value)}
            inputProps={{ min: 0, step: 0.1 }}
          />
        </Grid>
        <Grid size={{ xs: 4 }}>
          <TextField
            fullWidth
            type="number"
            label="Cholesterol (mg)"
            value={values.cholesterol_mg || ''}
            onChange={(e) => handleNumberChange('cholesterol_mg', e.target.value)}
            inputProps={{ min: 0 }}
          />
        </Grid>
      </Grid>

      <Divider sx={{ my: 2 }} />

      {/* Other Nutrients */}
      <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 'bold' }}>
        Other Nutrients
      </Typography>
      <Grid container spacing={2}>
        <Grid size={{ xs: 6 }}>
          <TextField
            fullWidth
            type="number"
            label="Sodium (mg)"
            value={values.sodium_mg || ''}
            onChange={(e) => handleNumberChange('sodium_mg', e.target.value)}
            inputProps={{ min: 0 }}
          />
        </Grid>
        <Grid size={{ xs: 6 }}>
          <TextField
            fullWidth
            type="number"
            label="Fiber (g)"
            value={values.fiber_g || ''}
            onChange={(e) => handleNumberChange('fiber_g', e.target.value)}
            inputProps={{ min: 0, step: 0.1 }}
          />
        </Grid>
        <Grid size={{ xs: 6 }}>
          <TextField
            fullWidth
            type="number"
            label="Sugar (g)"
            value={values.sugar_g || ''}
            onChange={(e) => handleNumberChange('sugar_g', e.target.value)}
            inputProps={{ min: 0, step: 0.1 }}
          />
        </Grid>
      </Grid>

      <Divider sx={{ my: 2 }} />

      {/* Vitamins & Minerals */}
      <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 'bold' }}>
        Vitamins & Minerals
      </Typography>
      <Grid container spacing={2}>
        <Grid size={{ xs: 6 }}>
          <TextField
            fullWidth
            type="number"
            label="Vitamin A (mcg)"
            value={values.vitamin_a_mcg || ''}
            onChange={(e) => handleNumberChange('vitamin_a_mcg', e.target.value)}
            inputProps={{ min: 0 }}
          />
        </Grid>
        <Grid size={{ xs: 6 }}>
          <TextField
            fullWidth
            type="number"
            label="Vitamin C (mg)"
            value={values.vitamin_c_mg || ''}
            onChange={(e) => handleNumberChange('vitamin_c_mg', e.target.value)}
            inputProps={{ min: 0, step: 0.1 }}
          />
        </Grid>
        <Grid size={{ xs: 6 }}>
          <TextField
            fullWidth
            type="number"
            label="Calcium (mg)"
            value={values.calcium_mg || ''}
            onChange={(e) => handleNumberChange('calcium_mg', e.target.value)}
            inputProps={{ min: 0 }}
          />
        </Grid>
        <Grid size={{ xs: 6 }}>
          <TextField
            fullWidth
            type="number"
            label="Iron (mg)"
            value={values.iron_mg || ''}
            onChange={(e) => handleNumberChange('iron_mg', e.target.value)}
            inputProps={{ min: 0, step: 0.1 }}
          />
        </Grid>
      </Grid>

      <Divider sx={{ my: 2 }} />

      {/* Cost */}
      <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 'bold' }}>
        Cost Information
      </Typography>
      <TextField
        fullWidth
        type="number"
        label="Cost per Serving ($)"
        value={values.cost_per_serving || ''}
        onChange={(e) => handleNumberChange('cost_per_serving', e.target.value)}
        inputProps={{ min: 0, step: 0.01 }}
      />
    </Paper>
  );
}
