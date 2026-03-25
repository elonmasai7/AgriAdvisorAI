import { useCallback, useMemo, useState } from "react";
import { useDropzone } from "react-dropzone";

function formatSize(sizeInBytes) {
  if (!sizeInBytes) return "0 KB";
  const mb = sizeInBytes / (1024 * 1024);
  if (mb >= 1) return `${mb.toFixed(2)} MB`;
  return `${(sizeInBytes / 1024).toFixed(1)} KB`;
}

export default function UploadZone({ onFileChange }) {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");

  const onDrop = useCallback(
    (acceptedFiles) => {
      const selected = acceptedFiles?.[0];
      if (!selected) return;

      setFile(selected);
      onFileChange(selected);

      const objectUrl = URL.createObjectURL(selected);
      setPreview(objectUrl);
    },
    [onFileChange],
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    multiple: false,
    accept: {
      "image/*": [],
    },
  });

  const borderClass = useMemo(() => {
    return isDragActive
      ? "border-green-500 bg-green-50"
      : "border-gray-300 hover:border-green-400";
  }, [isDragActive]);

  const clearFile = () => {
    setFile(null);
    setPreview("");
    onFileChange(null);
  };

  return (
    <div className="space-y-3">
      <div
        {...getRootProps()}
        className={`rounded-xl border-2 border-dashed p-5 text-center transition ${borderClass}`}
      >
        <input {...getInputProps()} />
        {preview ? (
          <div className="flex flex-col items-center gap-2">
            <img
              src={preview}
              alt="Crop preview"
              className="h-36 w-36 rounded-lg object-cover"
            />
            <p className="text-sm text-gray-700">
              {file?.name} ({formatSize(file?.size)})
            </p>
          </div>
        ) : (
          <div className="space-y-1">
            <p className="font-medium text-gray-700">
              Drag and drop a crop photo, or click to upload
            </p>
            <p className="text-sm text-gray-500">JPG, PNG, WEBP up to camera size</p>
          </div>
        )}
      </div>

      {file && (
        <button
          type="button"
          onClick={clearFile}
          className="rounded-md bg-gray-200 px-3 py-2 text-sm font-medium text-gray-800 hover:bg-gray-300"
        >
          Clear image
        </button>
      )}
    </div>
  );
}
