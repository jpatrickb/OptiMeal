import { Card, CardContent, Typography, Chip, Stack, Divider } from '@mui/material';
import type { MealLogResponse } from '../../services/api/meals';

interface MealCardProps {
  meal: MealLogResponse;
}

export default function MealCard({ meal }: MealCardProps) {
  const totals = meal.nutrition_totals;

  return (
    <Card variant="outlined">
      <CardContent>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <Typography variant="h6">
            {meal.meal_name || meal.meal_type || 'Meal'} • {new Date(meal.logged_at).toLocaleString()}
          </Typography>
          <Stack direction="row" spacing={1}>
            {totals.total_calories != null && (
              <Chip label={`${Math.round(totals.total_calories)} kcal`} size="small" />
            )}
            {totals.total_protein_g != null && (
              <Chip label={`P ${Number(totals.total_protein_g).toFixed(1)}g`} size="small" />
            )}
            {totals.total_carbs_g != null && (
              <Chip label={`C ${Number(totals.total_carbs_g).toFixed(1)}g`} size="small" />
            )}
            {totals.total_fat_g != null && (
              <Chip label={`F ${Number(totals.total_fat_g).toFixed(1)}g`} size="small" />
            )}
          </Stack>
        </Stack>

        <Divider sx={{ my: 1.5 }} />

        <Stack spacing={0.5}>
          {meal.logged_items.map((it) => (
            <Typography key={it.id} variant="body2" color="text.secondary">
              {it.food_item_name} • {it.servings} servings
            </Typography>
          ))}
        </Stack>
      </CardContent>
    </Card>
  );
}
