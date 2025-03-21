import { useDropzone } from 'react-dropzone';
import { useState, useCallback } from 'react';
import axios from 'axios';
import { saveAs } from 'file-saver';

interface FileUploadProps {
  file: File | null;
  uploadStatus: string;
}

export default function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string>('');
  const [heartRateData, setHeartRateData] = useState<any[]>([]); // For heart rate data
  const [loadingHeartRate, setLoadingHeartRate] = useState<boolean>(false); // For loading state
  const [aggregatedData, setAggregatedData] = useState<{ average: number, min: number, max: number } | null>(null);

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

  const handleFetchHeartRate = async () => {
    setLoadingHeartRate(true);
    try {
      const response = await axios.get('http://127.0.0.1:5000/fetch-heart-rate');
      const fetchedHeartRateData = response.data.heart_rate_data;
      setHeartRateData(fetchedHeartRateData);
      aggregateHeartRateData(fetchedHeartRateData); // Aggregate data after fetching
      setLoadingHeartRate(false);
    } catch (error) {
      console.error('Error fetching heart rate data:', error);
      setLoadingHeartRate(false);
    }
  };

  // Function to aggregate heart rate data
  const aggregateHeartRateData = (data: any[]) => {
    const values = data.map(item => parseFloat(item.value));

    const total = values.reduce((acc, curr) => acc + curr, 0);
    const average = values.length ? total / values.length : 0;
    const min = Math.min(...values);
    const max = Math.max(...values);

    setAggregatedData({
      average: average,
      min: min,
      max: max,
    });
  };

  // Save the heart rate data to a JSON file
  const handleSaveHeartRateAsJson = () => {
    const jsonData = JSON.stringify(heartRateData, null, 2); // Pretty print the JSON
    const blob = new Blob([jsonData], { type: 'application/json' });
    saveAs(blob, 'heart_rate_data.json');
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

      <hr />

      {/* Heart Rate Data Fetching */}
      <h2>Fetch Heart Rate Data</h2>
      <button onClick={handleFetchHeartRate}>
        {loadingHeartRate ? 'Loading Heart Rate Data...' : 'Fetch Heart Rate Data'}
      </button>

      {heartRateData.length > 0 && (
        <>
          <ul>
            {heartRateData.map((record, index) => (
              <li key={index}>
                {`Value: ${record.value}, Start: ${new Date(record.startDate).toLocaleString()}, End: ${new Date(record.endDate).toLocaleString()}`}
              </li>
            ))}
          </ul>

          {/* Aggregated Data */}
          {aggregatedData && (
            <div>
              <h3>Aggregated Data</h3>
              <p>Average Heart Rate: {aggregatedData.average.toFixed(2)}</p>
              <p>Minimum Heart Rate: {aggregatedData.min}</p>
              <p>Maximum Heart Rate: {aggregatedData.max}</p>
            </div>
          )}

          <button onClick={handleSaveHeartRateAsJson}>Save as JSON</button>
        </>
      )}
    </div>
  );
}
