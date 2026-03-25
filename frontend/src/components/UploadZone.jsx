import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

const UploadZone = ({ onFileChange }) => {
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);

    const onDrop = useCallback((acceptedFiles) => {
        const selectedFile = acceptedFiles[0];
        setFile(selectedFile);
        onFileChange(selectedFile);

        const reader = new FileReader();
        reader.onload = () => setPreview(reader.result);
        reader.readAsDataURL(selectedFile);
    }, [onFileChange]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: 'image/*',
        multiple: false,
    });

    const clearFile = () => {
        setFile(null);
        setPreview(null);
        onFileChange(null);
    };

    return (
        <div className="w-full">
            <div
                {...getRootProps()}
                className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${isDragActive ? 'border-green-500 bg-green-50' : 'border-gray-300 hover:border-green-400'
                    }`}
            >
                <input {...getInputProps()} />
                {preview ? (
                    <div className="flex flex-col items-center">
                        <img src={preview} alt="Preview" className="w-32 h-32 object-cover rounded mb-2" />
                        <p className="text-sm text-gray-600">{file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)</p>
                    </div>
                ) : (
                    <div>
                        <p className="text-gray-600 mb-2">
                            {isDragActive ? 'Drop the image here...' : 'Drag & drop a crop image here, or click to select'}
                        </p>
                        <p className="text-sm text-gray-500">Supported formats: JPG, PNG, GIF</p>
                    </div>
                )}
            </div>
            {file && (
                <button
                    onClick={clearFile}
                    className="mt-2 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
                >
                    Clear Image
                </button>
            )}
        </div>
    );
};

export default UploadZone;