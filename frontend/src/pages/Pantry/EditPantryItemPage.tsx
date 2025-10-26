import { useState, useEffect, type FormEvent } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Alert,
  CircularProgress,
  Container,
  TextField,
  Grid,
  MenuItem,
  Paper,
} from '@mui/material';
import { ArrowBack as ArrowBackIcon, Save as SaveIcon } from '@mui/icons-material';
import type { PantryItemWithFood, PantryItemUpdate } from '../../types';
import { pantryApi } from '../../services/api/pantry';

const STORAGE_LOCATIONS = ['Pantry', 'Fridge', 'Freezer', 'Cabinet'];

export default function EditPantryItemPage() {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const [pantryItem, setPantryItem] = useState<PantryItemWithFood | null>(null);
  const [quantity, setQuantity] = useState<string>('');
  const [unit, setUnit] = useState<string>('');
  const [expirationDate, setExpirationDate] = useState<string>('');
  const [location, setLocation] = useState<string>('Pantry');
  const [loading, setLoading] = useState(false);
  const [loadingItem, setLoadingItem] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (id) {
      loadPantryItem();
    }
  }, [id]);

  const loadPantryItem = async () => {
    if (!id) return;

    try {
      setLoadingItem(true);
      const items = await pantryApi.list();
      const item = items.find((i) => i.id === id);

      if (!item) {
        setError('Pantry item not found');
        return;
      }

      setPantryItem(item);
      setQuantity(item.quantity.toString());
      setUnit(item.unit);
      setExpirationDate(item.expiration_date || '');
      setLocation(item.location || 'Pantry');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load pantry item');
    } finally {
      setLoadingItem(false);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');

    if (!id) return;

    if (!quantity || parseFloat(quantity) < 0) {
      setError('Please enter a valid quantity (must be 0 or greater)');
      return;
    }

    if (!unit) {
      setError('Please enter a unit');
      return;
    }

    setLoading(true);

    try {
      const updateData: PantryItemUpdate = {
        quantity: parseFloat(quantity),
        unit,
        expiration_date: expirationDate || undefined,
        location: location || undefined,
      };

      await pantryApi.update(id, updateData);
      navigate('/pantry');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update pantry item. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (loadingItem) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '50vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!pantryItem) {
    return (
      <Container maxWidth="md">
        <Box sx={{ mb: 3 }}>
          <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/pantry')}>
            Back to Pantry
          </Button>
        </Box>
        <Alert severity="error">Pantry item not found</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ mb: 3 }}>
        <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/pantry')}>
          Back to Pantry
        </Button>
      </Box>

      <Typography variant="h4" component="h1" gutterBottom>
        Edit Pantry Item
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          {pantryItem.food_item.name}
        </Typography>
        {pantryItem.food_item.brand && (
          <Typography variant="body2" color="text.secondary">
            Brand: {pantryItem.food_item.brand}
          </Typography>
        )}
        <Typography variant="body2" color="text.secondary">
          Serving: {pantryItem.food_item.serving_size} {pantryItem.food_item.serving_unit}
        </Typography>
      </Paper>

      <Box component="form" onSubmit={handleSubmit}>
        <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
          Update Quantity and Details
        </Typography>

        <Grid container spacing={2}>
          <Grid size={{ xs: 12, sm: 6 }}>
            <TextField
              fullWidth
              required
              type="number"
              label="Quantity"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              inputProps={{ min: 0, step: 0.1 }}
              helperText="Set to 0 to mark as depleted"
            />
          </Grid>
          <Grid size={{ xs: 12, sm: 6 }}>
            <TextField
              fullWidth
              required
              label="Unit"
              value={unit}
              onChange={(e) => setUnit(e.target.value)}
              placeholder="cup, oz, g, etc."
            />
          </Grid>
        </Grid>

        <TextField
          fullWidth
          type="date"
          label="Expiration Date (optional)"
          value={expirationDate}
          onChange={(e) => setExpirationDate(e.target.value)}
          margin="normal"
          InputLabelProps={{ shrink: true }}
        />

        <TextField
          fullWidth
          select
          label="Storage Location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          margin="normal"
        >
          {STORAGE_LOCATIONS.map((loc) => (
            <MenuItem key={loc} value={loc}>
              {loc}
            </MenuItem>
          ))}
        </TextField>

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
            {loading ? 'Saving...' : 'Save Changes'}
          </Button>
        </Box>
      </Box>
    </Container>
  );
}
