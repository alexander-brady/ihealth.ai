'use client';

import { useDropzone } from 'react-dropzone';
import { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation'; // Import from 'next/navigation' for Next.js 13+ in app directory
import axios from 'axios';

export default function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string>('');

  const router = useRouter(); // Initialize the router

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
        // Redirect to chat page after successful upload
        router.push('/chat'); // Redirect to /chat
      } catch (error) {
        setUploadStatus('File upload failed');
      }
    } else {
      setUploadStatus('No file selected');
    }
  };

  return (
    <div className="max-w-screen-xl mx-auto py-20 px-5">
      <h1 className="text-3xl font-bold mb-5">Upload your Apple Watch Health Data</h1>
      <div
        {...getRootProps()}
        className="flex flex-col items-center justify-center border-2 border-dashed border-gray-400 p-20 cursor-pointer text-center w-full h-64 mt-5"
      >
        <input {...getInputProps()} />
        <p className="font-semibold">Drag 'n' drop a file here, or click to select one</p>
      </div>
      {file && <p className="mt-2">Selected file: <strong>{file.name}</strong></p>}

      {/* Small, compact button */}
      <button
        onClick={handleUpload}
        className="px-4 py-2 text-white bg-blue-600 hover:bg-blue-700 rounded-md mt-4"
      >
        Upload
      </button>

      <p className="mt-2">{uploadStatus}</p>

      <hr className="my-10" />

      <h2 className="text-lg font-bold">Instructions for Uploading</h2>
      <ol className="list-decimal ml-5 mt-2">
        <li>Open the Health app on your iPhone.</li>
        <li>Click on your profile picture.</li>
        <li>Select "Export All Health Data."</li>
        <li>Upload the <code>exporter.xml</code> file to this application.</li>
      </ol>
    </div>
  );
}
