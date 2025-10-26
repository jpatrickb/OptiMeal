import { useState, useEffect, type FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Alert,
  CircularProgress,
  Container,
  TextField,
  Autocomplete,
  Grid,
  MenuItem,
} from '@mui/material';
import { ArrowBack as ArrowBackIcon, Add as AddIcon } from '@mui/icons-material';
import type { FoodItem, PantryItemCreate } from '../../types';
import { foodItemsApi } from '../../services/api/foodItems';
import { pantryApi } from '../../services/api/pantry';

const STORAGE_LOCATIONS = ['Pantry', 'Fridge', 'Freezer', 'Cabinet'];

export default function AddToPantryPage() {
  const navigate = useNavigate();
  const [foodItems, setFoodItems] = useState<FoodItem[]>([]);
  const [selectedFood, setSelectedFood] = useState<FoodItem | null>(null);
  const [quantity, setQuantity] = useState<string>('');
  const [unit, setUnit] = useState<string>('');
  const [expirationDate, setExpirationDate] = useState<string>('');
  const [location, setLocation] = useState<string>('Pantry');
  const [loading, setLoading] = useState(false);
  const [loadingFoodItems, setLoadingFoodItems] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadFoodItems();
  }, []);

  useEffect(() => {
    // Auto-fill unit when food item is selected
    if (selectedFood) {
      setUnit(selectedFood.serving_unit);
    }
  }, [selectedFood]);

  const loadFoodItems = async () => {
    try {
      setLoadingFoodItems(true);
      const items = await foodItemsApi.list();
      setFoodItems(items);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load food items');
    } finally {
      setLoadingFoodItems(false);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');

    if (!selectedFood) {
      setError('Please select a food item');
      return;
    }

    if (!quantity || parseFloat(quantity) <= 0) {
      setError('Please enter a valid quantity');
      return;
    }

    if (!unit) {
      setError('Please enter a unit');
      return;
    }

    setLoading(true);

    try {
      const pantryItemData: PantryItemCreate = {
        food_item_id: selectedFood.id,
        quantity: parseFloat(quantity),
        unit,
        expiration_date: expirationDate || undefined,
        location: location || undefined,
      };

      await pantryApi.add(pantryItemData);
      navigate('/pantry');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to add item to pantry. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (loadingFoodItems) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '50vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (foodItems.length === 0) {
    return (
      <Container maxWidth="md">
        <Box sx={{ mb: 3 }}>
          <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/pantry')}>
            Back to Pantry
          </Button>
        </Box>

        <Box sx={{ textAlign: 'center', py: 8 }}>
          <Typography variant="h5" gutterBottom>
            No Food Items Available
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
            You need to create food items before adding them to your pantry.
          </Typography>
          <Button variant="contained" onClick={() => navigate('/pantry/add-food-item')}>
            Create Food Item
          </Button>
        </Box>
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
        Add to Pantry
      </Typography>

      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Select an existing food item and specify the quantity you have in your pantry.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      <Box component="form" onSubmit={handleSubmit}>
        <Autocomplete
          options={foodItems}
          getOptionLabel={(option) => `${option.name}${option.brand ? ` (${option.brand})` : ''}`}
          value={selectedFood}
          onChange={(_, newValue) => setSelectedFood(newValue)}
          renderInput={(params) => (
            <TextField {...params} label="Select Food Item" required fullWidth margin="normal" />
          )}
          fullWidth
        />

        <Grid container spacing={2} sx={{ mt: 2 }}>
          <Grid size={{ xs: 12, sm: 6 }}>
            <TextField
              fullWidth
              required
              type="number"
              label="Quantity"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              inputProps={{ min: 0, step: 0.1 }}
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
            startIcon={loading ? <CircularProgress size={20} /> : <AddIcon />}
            disabled={loading}
          >
            {loading ? 'Adding...' : 'Add to Pantry'}
          </Button>
        </Box>
      </Box>
    </Container>
  );
}
