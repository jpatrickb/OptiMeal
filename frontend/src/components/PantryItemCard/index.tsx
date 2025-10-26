import {
  Card,
  CardContent,
  Typography,
  Chip,
  Box,
  Grid,
  IconButton,
  CardActions,
} from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon, Warning as WarningIcon } from '@mui/icons-material';
import type { PantryItemWithFood } from '../../types';

interface PantryItemCardProps {
  pantryItem: PantryItemWithFood;
  onEdit?: () => void;
  onDelete?: () => void;
}

export default function PantryItemCard({ pantryItem, onEdit, onDelete }: PantryItemCardProps) {
  const { food_item } = pantryItem;

  // Check if item is expiring soon (within 3 days)
  const isExpiringSoon = () => {
    if (!pantryItem.expiration_date) return false;
    const expDate = new Date(pantryItem.expiration_date);
    const today = new Date();
    const threeDaysFromNow = new Date();
    threeDaysFromNow.setDate(today.getDate() + 3);
    return expDate <= threeDaysFromNow && expDate >= today;
  };

  const isExpired = () => {
    if (!pantryItem.expiration_date) return false;
    const expDate = new Date(pantryItem.expiration_date);
    const today = new Date();
    return expDate < today;
  };

  const formatExpirationDate = (date: string) => {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  return (
    <Card
      sx={{
        position: 'relative',
        border: isExpired() ? '2px solid #f44336' : isExpiringSoon() ? '2px solid #ff9800' : 'none',
      }}
    >
      <CardContent>
        {(isExpired() || isExpiringSoon()) && (
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <WarningIcon
              sx={{
                color: isExpired() ? 'error.main' : 'warning.main',
                mr: 1,
              }}
            />
            <Typography
              variant="caption"
              sx={{ color: isExpired() ? 'error.main' : 'warning.main', fontWeight: 'bold' }}
            >
              {isExpired() ? 'EXPIRED' : 'EXPIRING SOON'}
            </Typography>
          </Box>
        )}

        <Typography variant="h6" component="div" gutterBottom>
          {food_item.name}
        </Typography>
        {food_item.brand && (
          <Typography variant="body2" color="text.secondary" gutterBottom>
            {food_item.brand}
          </Typography>
        )}

        <Box sx={{ mt: 2 }}>
          <Grid container spacing={1}>
            <Grid size={{ xs: 12 }}>
              <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                Quantity: {pantryItem.quantity} {pantryItem.unit}
              </Typography>
            </Grid>
            {pantryItem.expiration_date && (
              <Grid size={{ xs: 12 }}>
                <Typography variant="body2" color="text.secondary">
                  Expires: {formatExpirationDate(pantryItem.expiration_date)}
                </Typography>
              </Grid>
            )}
            {pantryItem.location && (
              <Grid size={{ xs: 12 }}>
                <Chip label={pantryItem.location} size="small" />
              </Grid>
            )}
          </Grid>
        </Box>

        {(food_item.calories !== undefined ||
          food_item.protein_g !== undefined ||
          food_item.carbs_g !== undefined ||
          food_item.fat_g !== undefined) && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="caption" color="text.secondary" gutterBottom>
              Per serving ({food_item.serving_size} {food_item.serving_unit}):
            </Typography>
            <Grid container spacing={0.5} sx={{ mt: 0.5 }}>
              {food_item.calories !== undefined && (
                <Grid>
                  <Chip label={`${food_item.calories} cal`} size="small" />
                </Grid>
              )}
              {food_item.protein_g !== undefined && (
                <Grid>
                  <Chip label={`${food_item.protein_g}g protein`} size="small" color="primary" />
                </Grid>
              )}
              {food_item.carbs_g !== undefined && (
                <Grid>
                  <Chip label={`${food_item.carbs_g}g carbs`} size="small" color="secondary" />
                </Grid>
              )}
              {food_item.fat_g !== undefined && (
                <Grid>
                  <Chip label={`${food_item.fat_g}g fat`} size="small" color="warning" />
                </Grid>
              )}
            </Grid>
          </Box>
        )}
      </CardContent>

      {(onEdit || onDelete) && (
        <CardActions sx={{ justifyContent: 'flex-end', pt: 0 }}>
          {onEdit && (
            <IconButton size="small" onClick={onEdit} color="primary">
              <EditIcon />
            </IconButton>
          )}
          {onDelete && (
            <IconButton size="small" onClick={onDelete} color="error">
              <DeleteIcon />
            </IconButton>
          )}
        </CardActions>
      )}
    </Card>
  );
}
