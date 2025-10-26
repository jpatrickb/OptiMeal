import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Grid,
  CircularProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Fab,
  Menu,
  MenuItem,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import PantryItemCard from '../../components/PantryItemCard';
import type { PantryItemWithFood } from '../../types';
import { pantryApi } from '../../services/api/pantry';

export default function PantryPage() {
  const navigate = useNavigate();
  const [pantryItems, setPantryItems] = useState<PantryItemWithFood[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [itemToDelete, setItemToDelete] = useState<string | null>(null);
  const [addMenuAnchor, setAddMenuAnchor] = useState<null | HTMLElement>(null);

  useEffect(() => {
    loadPantryItems();
  }, []);

  const loadPantryItems = async () => {
    try {
      setLoading(true);
      setError('');
      const items = await pantryApi.list();
      setPantryItems(items);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load pantry items');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteClick = (id: string) => {
    setItemToDelete(id);
    setDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (!itemToDelete) return;

    try {
      await pantryApi.delete(itemToDelete);
      setPantryItems(pantryItems.filter((item) => item.id !== itemToDelete));
      setDeleteDialogOpen(false);
      setItemToDelete(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete pantry item');
      setDeleteDialogOpen(false);
    }
  };

  const handleAddClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAddMenuAnchor(event.currentTarget);
  };

  const handleAddMenuClose = () => {
    setAddMenuAnchor(null);
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '50vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          My Pantry
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      {pantryItems.length === 0 ? (
        <Box
          sx={{
            textAlign: 'center',
            py: 8,
            px: 2,
          }}
        >
          <Typography variant="h6" color="text.secondary" gutterBottom>
            Your pantry is empty
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Start by adding food items and then add them to your pantry
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => navigate('/pantry/add-food-item')}
          >
            Add Food Item
          </Button>
        </Box>
      ) : (
        <Grid container spacing={3}>
          {pantryItems.map((item) => (
            <Grid size={{ xs: 12, sm: 6, md: 4 }} key={item.id}>
              <PantryItemCard
                pantryItem={item}
                onEdit={() => navigate(`/pantry/edit/${item.id}`)}
                onDelete={() => handleDeleteClick(item.id)}
              />
            </Grid>
          ))}
        </Grid>
      )}

      {/* Floating Action Button */}
      <Fab
        color="primary"
        aria-label="add"
        sx={{ position: 'fixed', bottom: 16, right: 16 }}
        onClick={handleAddClick}
      >
        <AddIcon />
      </Fab>

      {/* Add Menu */}
      <Menu anchorEl={addMenuAnchor} open={Boolean(addMenuAnchor)} onClose={handleAddMenuClose}>
        <MenuItem
          onClick={() => {
            handleAddMenuClose();
            navigate('/pantry/add-food-item');
          }}
        >
          Create New Food Item
        </MenuItem>
        <MenuItem
          onClick={() => {
            handleAddMenuClose();
            navigate('/pantry/add-to-pantry');
          }}
        >
          Add Existing Item to Pantry
        </MenuItem>
      </Menu>

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Delete Pantry Item</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to remove this item from your pantry? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleDeleteConfirm} color="error" autoFocus>
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
