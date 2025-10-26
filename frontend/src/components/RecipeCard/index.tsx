import { Card, CardContent, Typography } from '@mui/material';

interface RecipeCardProps {
  name: string;
  description?: string;
  calories?: number | null;
}

export default function RecipeCard({ name, description, calories }: RecipeCardProps) {
  return (
    <Card variant="outlined">
      <CardContent>
        <Typography variant="h6">{name}</Typography>
        {description && (
          <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
            {description}
          </Typography>
        )}
        {calories != null && (
          <Typography variant="body2" sx={{ mt: 1 }}>
            ~{Math.round(calories)} kcal
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}
