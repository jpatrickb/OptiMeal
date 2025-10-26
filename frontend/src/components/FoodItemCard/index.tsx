import { Card, CardContent, Typography, Chip, Box, Grid } from '@mui/material';
import type { FoodItem } from '../../types';

interface FoodItemCardProps {
  foodItem: FoodItem;
  onClick?: () => void;
}

export default function FoodItemCard({ foodItem, onClick }: FoodItemCardProps) {
  const hasNutrition =
    foodItem.calories !== undefined ||
    foodItem.protein_g !== undefined ||
    foodItem.carbs_g !== undefined ||
    foodItem.fat_g !== undefined;

  return (
    <Card
      sx={{
        cursor: onClick ? 'pointer' : 'default',
        '&:hover': onClick ? { boxShadow: 6 } : {},
        transition: 'box-shadow 0.3s',
      }}
      onClick={onClick}
    >
      <CardContent>
        <Typography variant="h6" component="div" gutterBottom>
          {foodItem.name}
        </Typography>
        {foodItem.brand && (
          <Typography variant="body2" color="text.secondary" gutterBottom>
            {foodItem.brand}
          </Typography>
        )}
        <Typography variant="body2" color="text.secondary" gutterBottom>
          Serving: {foodItem.serving_size} {foodItem.serving_unit}
        </Typography>

        {hasNutrition && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" gutterBottom>
              Nutrition Facts (per serving)
            </Typography>
            <Grid container spacing={1}>
              {foodItem.calories !== undefined && (
                <Grid size={{ xs: 6 }}>
                  <Chip label={`${foodItem.calories} cal`} size="small" />
                </Grid>
              )}
              {foodItem.protein_g !== undefined && (
                <Grid size={{ xs: 6 }}>
                  <Chip label={`${foodItem.protein_g}g protein`} size="small" color="primary" />
                </Grid>
              )}
              {foodItem.carbs_g !== undefined && (
                <Grid size={{ xs: 6 }}>
                  <Chip label={`${foodItem.carbs_g}g carbs`} size="small" color="secondary" />
                </Grid>
              )}
              {foodItem.fat_g !== undefined && (
                <Grid size={{ xs: 6 }}>
                  <Chip label={`${foodItem.fat_g}g fat`} size="small" color="warning" />
                </Grid>
              )}
            </Grid>
          </Box>
        )}

        {foodItem.cost_per_serving !== undefined && foodItem.cost_per_serving !== null && (
          <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
            Cost: ${foodItem.cost_per_serving.toFixed(2)}/serving
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}
