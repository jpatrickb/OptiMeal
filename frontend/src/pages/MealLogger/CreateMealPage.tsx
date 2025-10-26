import { useEffect, useMemo, useState } from 'react';
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Container,
  Divider,
  MenuItem,
  Select,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
// Using native Date functions to avoid extra deps
import FoodItemSelector, { type SelectedItem } from '../../components/FoodItemSelector';
import { foodItemsApi, type FoodItemResponse } from '../../services/api/foodItems';
import { mealsApi } from '../../services/api/meals';
import { recipesApi, type RecipeListItem } from '../../services/api/recipes';

export default function CreateMealPage() {
  const [items, setItems] = useState<Array<SelectedItem & { food?: FoodItemResponse }>>([]);
  const [mealType, setMealType] = useState<'breakfast' | 'lunch' | 'dinner' | 'snack' | ''>('');
  const [loggedAt, setLoggedAt] = useState<string>(new Date().toISOString());
  const [notes, setNotes] = useState('');
  const [error, setError] = useState('');
  const [warnings, setWarnings] = useState<string[]>([]);
  const [recipes, setRecipes] = useState<RecipeListItem[]>([]);
  const [selectedRecipeId, setSelectedRecipeId] = useState('');

  useEffect(() => {
    (async () => {
      const res = await recipesApi.list({ page: 1, per_page: 50 });
      setRecipes(res.recipes);
    })();
  }, []);

  const totals = useMemo(() => {
    const sum = { calories: 0, protein: 0, carbs: 0, fat: 0 };
    for (const it of items) {
      if (it.food) {
        sum.calories += (it.food.calories || 0) * it.servings;
        sum.protein += (it.food.protein_g || 0) * it.servings;
        sum.carbs += (it.food.carbs_g || 0) * it.servings;
        sum.fat += (it.food.fat_g || 0) * it.servings;
      }
    }
    return sum;
  }, [items]);

  const addItem = async (item: SelectedItem) => {
    const food = await foodItemsApi.getById(item.food_item_id);
    setItems((prev) => [...prev, { ...item, food }]);
  };

  const addRecipe = async (recipeId: string) => {
    const recipe = await recipesApi.getById(recipeId);
const toAdd: Array<SelectedItem & { food?: FoodItemResponse }> = [];
    for (const ing of recipe.ingredients) {
      const food = await foodItemsApi.getById(ing.food_item_id);
      toAdd.push({ food_item_id: ing.food_item_id, servings: ing.servings, food });
    }
    setItems((prev) => [...prev, ...toAdd]);
  };

  const submit = async () => {
    setError('');
    setWarnings([]);
    if (items.length === 0) {
      setError('Add at least one item to log a meal.');
      return;
    }
    try {
      const payload = {
        meal_type: mealType || undefined,
        logged_at: loggedAt,
        notes: notes || undefined,
        items: items.map((i) => ({ food_item_id: i.food_item_id, servings: i.servings })),
      };
      const res = await mealsApi.create(payload);
      if (res.warnings?.length) {
        setWarnings(res.warnings.map((w) => w.message));
      }
      window.location.href = '/meal-logger';
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Failed to log meal');
    }
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h4" sx={{ mb: 2 }}>
        Create Meal
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}
      {warnings.map((w, idx) => (
        <Alert key={idx} severity="warning" sx={{ mb: 1 }}>
          {w}
        </Alert>
      ))}

      <Card variant="outlined" sx={{ mb: 2 }}>
        <CardContent>
          <Stack spacing={2}>
            <Stack direction="row" spacing={2}>
              <Select
                displayEmpty
                value={mealType}
                onChange={(e) => setMealType(e.target.value as any)}
                size="small"
              >
                <MenuItem value="">Select meal type</MenuItem>
                <MenuItem value="breakfast">Breakfast</MenuItem>
                <MenuItem value="lunch">Lunch</MenuItem>
                <MenuItem value="dinner">Dinner</MenuItem>
                <MenuItem value="snack">Snack</MenuItem>
              </Select>
              <TextField
                type="datetime-local"
                size="small"
                value={new Date(loggedAt).toISOString().slice(0, 16)}
                onChange={(e) => {
                  const v = e.target.value;
                  // Keep as local datetime by appending :00Z then adjusting
                  const iso = new Date(v).toISOString();
                  setLoggedAt(iso);
                }}
              />
              <TextField
                placeholder="Notes (optional)"
                fullWidth
                size="small"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
              />
            </Stack>

            <Divider />

            <FoodItemSelector onAdd={addItem} />

            <Stack direction="row" spacing={2} alignItems="center">
              <Select
                displayEmpty
                value={selectedRecipeId}
                onChange={async (e) => {
                  const id = e.target.value as string;
                  setSelectedRecipeId(id);
                  if (id) await addRecipe(id);
                }}
                size="small"
              >
                <MenuItem value="">Add from recipe...</MenuItem>
                {recipes.map((r) => (
                  <MenuItem key={r.id} value={r.id}>
                    {r.name}
                  </MenuItem>
                ))}
              </Select>
              <Typography variant="body2" color="text.secondary">
                Add a saved recipe to this meal
              </Typography>
            </Stack>

            <Divider />

            <Stack spacing={1}>
              {items.map((i, idx) => (
                <Typography key={`${i.food_item_id}-${idx}`} variant="body2">
                  {i.food?.name} — {i.servings} serving(s)
                </Typography>
              ))}
            </Stack>

            <Divider />

            <Typography>
              Totals: {Math.round(totals.calories)} kcal • P {totals.protein.toFixed(1)}g • C {totals.carbs.toFixed(1)}g • F {totals.fat.toFixed(1)}g
            </Typography>

            <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 1 }}>
              <Button variant="outlined" href="/meal-logger">
                Cancel
              </Button>
              <Button variant="contained" onClick={submit}>
                Log Meal
              </Button>
            </Box>
          </Stack>
        </CardContent>
      </Card>
    </Container>
  );
}
