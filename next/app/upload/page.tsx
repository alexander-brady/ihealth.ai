'use client';

import { useDropzone } from 'react-dropzone';
import { useState, useCallback } from 'react';
import axios from 'axios';
import { saveAs } from 'file-saver';
import SectionHeading from "./../components/core/sectionHeading";
import Button from "./../components/core/button";
import { FaUpload } from 'react-icons/fa'; // Assuming you're using a package for icons

export default function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string>('');
  const [heartRateData, setHeartRateData] = useState<any[]>([]);
  const [loadingHeartRate, setLoadingHeartRate] = useState<boolean>(false);
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
        await axios.post('flask/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
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
      const response = await axios.get('flask/fetch-heart-rate');
      const fetchedHeartRateData = response.data.heart_rate_data;
      setHeartRateData(fetchedHeartRateData);
      aggregateHeartRateData(fetchedHeartRateData);
      setLoadingHeartRate(false);
    } catch (error) {
      console.error('Error fetching heart rate data:', error);
      setLoadingHeartRate(false);
    }
  };

  const aggregateHeartRateData = (data: any[]) => {
    const values = data.map(item => parseFloat(item.value));
    const total = values.reduce((acc, curr) => acc + curr, 0);
    const average = values.length ? total / values.length : 0;
    const min = Math.min(...values);
    const max = Math.max(...values);
    setAggregatedData({ average, min, max });
  };

  const handleSaveHeartRateAsJson = () => {
    const jsonData = JSON.stringify(heartRateData, null, 2);
    const blob = new Blob([jsonData], { type: 'application/json' });
    saveAs(blob, 'heart_rate_data.json');
  };

  return (
    <div className="max-w-screen-xl mx-auto py-20 px-5">
      <SectionHeading text="Upload your Apple Watch Health Data" />
      <div
        {...getRootProps()}
        className="flex flex-col items-center justify-center border-2 border-dashed border-gray-400 p-20 cursor-pointer text-center w-full h-64 mt-5"
      >
        <input {...getInputProps()} />
        <FaUpload className="text-4xl mb-2" />
        <p className="font-semibold">Drag 'n' drop a file here, or click to select one</p>
      </div>
      {file && <p className="mt-2">Selected file: <strong>{file.name}</strong></p>}
      <Button text="Upload" stylingClass="py-3 px-5 text-white bg-blue-700 hover:bg-blue-800 mt-4" onClick={handleUpload} />
      <p className="mt-2">{uploadStatus}</p>

      <hr className="my-10" />

      <h2 className="text-lg font-bold">Instructions for Uploading</h2>
      <ol className="list-decimal ml-5 mt-2">
        <li>Open the Health app on your iPhone.</li>
        <li>Click on your profile picture.</li>
        <li>Select "Export All Health Data."</li>
        <li>Upload the <code>exporter.xml</code> file to this application.</li>
      </ol>

      {heartRateData.length > 0 && (
        <>
          <ul className="mt-4">
            {heartRateData.map((record, index) => (
              <li key={index}>
                {`Value: ${record.value}, Start: ${new Date(record.startDate).toLocaleString()}, End: ${new Date(record.endDate).toLocaleString()}`}
              </li>
            ))}
          </ul>

          {aggregatedData && (
            <div className="mt-4">
              <h3 className="text-lg font-semibold">Aggregated Data</h3>
              <p>Average Heart Rate: {aggregatedData.average.toFixed(2)}</p>
              <p>Minimum Heart Rate: {aggregatedData.min}</p>
              <p>Maximum Heart Rate: {aggregatedData.max}</p>
            </div>
          )}

          <Button text="Save as JSON" stylingClass="py-3 px-5 text-white bg-blue-700 hover:bg-blue-800 mt-4" onClick={handleSaveHeartRateAsJson} />
        </>
      )}
    </div>
  );
}
