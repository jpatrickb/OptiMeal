import { Box, Button } from '@mui/material';
import { useRef, useState } from 'react';

interface ImageUploadButtonProps {
  onFileSelected: (file: File) => void;
}

export default function ImageUploadButton({ onFileSelected }: ImageUploadButtonProps) {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  return (
    <Box>
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        style={{ display: 'none' }}
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) {
            setPreviewUrl(URL.createObjectURL(file));
            onFileSelected(file);
          }
        }}
      />
      <Button variant="outlined" onClick={() => inputRef.current?.click()}>Upload Nutrition Label</Button>
      {previewUrl && (
        <Box sx={{ mt: 1 }}>
          <img src={previewUrl} alt="preview" style={{ maxWidth: '100%', maxHeight: 200 }} />
        </Box>
      )}
    </Box>
  );
}
