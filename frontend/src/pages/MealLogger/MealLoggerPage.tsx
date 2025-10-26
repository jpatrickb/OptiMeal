import { useEffect, useState } from 'react';
import { Box, Button, Container, Stack, Typography, Alert } from '@mui/material';
import MealCard from '../../components/MealCard';
import { mealsApi, type MealLogResponse, type MealLogListResponse } from '../../services/api/meals';
import { recipesApi } from '../../services/api/recipes';

export default function MealLoggerPage() {
  const [data, setData] = useState<MealLogListResponse | null>(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const load = async () => {
    try {
      const res = await mealsApi.list({ page: 1, per_page: 20 });
      setData(res);
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Failed to load meals');
    }
  };

  useEffect(() => {
    load();
  }, []);

  const saveAsRecipe = async (meal: MealLogResponse) => {
    try {
      const name = meal.meal_name || `Meal ${new Date(meal.logged_at).toLocaleString()}`;
      await recipesApi.createFromMeal({ name, meal_log_id: meal.id });
      setSuccess('Saved as recipe');
      setTimeout(() => setSuccess(''), 2000);
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Failed to save as recipe');
    }
  };

  return (
    <Container maxWidth="md">
      <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
        <Typography variant="h4">Meal History</Typography>
        <Button variant="contained" href="/meal-logger/create">Log Meal</Button>
      </Stack>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}
      {success && (
        <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess('')}>
          {success}
        </Alert>
      )}

      <Stack spacing={2}>
        {data?.meals.map((meal) => (
          <Box key={meal.id}>
            <MealCard meal={meal} />
            <Box sx={{ mt: 1, display: 'flex', gap: 1 }}>
              <Button size="small" variant="outlined" onClick={() => saveAsRecipe(meal)}>
                Save as Recipe
              </Button>
            </Box>
          </Box>
        ))}
      </Stack>
    </Container>
  );
}
