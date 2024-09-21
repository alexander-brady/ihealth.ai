import { useDropzone } from 'react-dropzone';
import { useState, useCallback } from 'react';
import axios from 'axios';

interface FileUploadProps {
  file: File | null;
  uploadStatus: string;
}

export default function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string>('');

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFile(acceptedFiles[0]);
  }, []);

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  const handleUpload = async () => {
    if (file) {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        setUploadStatus('File uploaded successfully');
      } catch (error) {
        setUploadStatus('File upload failed');
      }
    } else {
      setUploadStatus('No file selected');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Upload your XML file</h1>
      <div
        {...getRootProps()}
        style={{
          border: '2px dashed gray',
          padding: '20px',
          cursor: 'pointer',
        }}
      >
        <input {...getInputProps()} />
        <p>Drag 'n' drop a file here, or click to select one</p>
      </div>
      {file && <p>Selected file: {file.name}</p>}
      <button onClick={handleUpload}>Upload</button>
      <p>{uploadStatus}</p>
    </div>
  );
}
