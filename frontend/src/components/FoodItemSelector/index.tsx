import { Autocomplete, TextField, Grid, IconButton } from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { useEffect, useState } from 'react';
import { foodItemsApi, type FoodItemResponse } from '../../services/api/foodItems';

export interface SelectedItem {
  food_item_id: string;
  servings: number;
  display?: string;
}

interface FoodItemSelectorProps {
  onAdd: (item: SelectedItem) => void;
}

export default function FoodItemSelector({ onAdd }: FoodItemSelectorProps) {
  const [options, setOptions] = useState<FoodItemResponse[]>([]);
  const [selected, setSelected] = useState<FoodItemResponse | null>(null);
  const [servings, setServings] = useState<number>(1);

  useEffect(() => {
    (async () => {
      const items = await foodItemsApi.list({ limit: 100 });
      setOptions(items);
    })();
  }, []);

  return (
    <Grid container spacing={2} alignItems="center">
      <Grid size={{ xs: 8 }}>
        <Autocomplete
          options={options}
          getOptionLabel={(opt) => `${opt.name}${opt.brand ? ` (${opt.brand})` : ''}`}
          value={selected}
          onChange={(_, v) => setSelected(v)}
          renderInput={(params) => <TextField {...params} label="Search food items" />}
        />
      </Grid>
      <Grid size={{ xs: 3 }}>
        <TextField
          type="number"
          label="Servings"
          value={servings}
          onChange={(e) => setServings(Number(e.target.value))}
          inputProps={{ min: 0.1, step: 0.1 }}
          fullWidth
        />
      </Grid>
      <Grid size={{ xs: 1 }}>
        <IconButton
          color="primary"
          onClick={() => {
            if (selected && servings > 0) {
              onAdd({
                food_item_id: selected.id,
                servings,
                display: `${selected.name}${selected.brand ? ` (${selected.brand})` : ''}`,
              });
              setSelected(null);
              setServings(1);
            }
          }}
        >
          <AddIcon />
        </IconButton>
      </Grid>
    </Grid>
  );
}
