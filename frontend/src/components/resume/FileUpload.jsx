/**
 * FileUpload — drag-and-drop file upload with preview.
 */
import React, { useState, useRef } from 'react';

export default function FileUpload({ onFileSelect, disabled = false }) {
  const [dragOver, setDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const inputRef = useRef(null);

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) handleFile(file);
  };

  const handleFile = (file) => {
    if (file.type !== 'application/pdf') {
      alert('Only PDF files are accepted.');
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      alert('File size must be under 5MB.');
      return;
    }
    setSelectedFile(file);
    onFileSelect(file);
  };

  return (
    <div
      className={`relative border-2 border-dashed rounded-xl p-10 text-center transition-all duration-300 cursor-pointer
        ${dragOver ? 'border-brand-primary bg-brand-primary/5' : 'border-border-glass hover:border-brand-primary/50'}
        ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
      onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
      onDragLeave={() => setDragOver(false)}
      onDrop={handleDrop}
      onClick={() => !disabled && inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".pdf"
        className="hidden"
        onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
        disabled={disabled}
      />

      {selectedFile ? (
        <div className="slide-up">
          <div className="w-14 h-14 rounded-xl bg-brand-emerald/10 flex items-center justify-center mx-auto mb-3">
            <svg className="w-7 h-7 text-brand-emerald" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <p className="text-text-primary font-medium">{selectedFile.name}</p>
          <p className="text-text-secondary text-sm mt-1">{(selectedFile.size / 1024).toFixed(1)} KB</p>
          <p className="text-brand-primary text-xs mt-2">Click or drop to change file</p>
        </div>
      ) : (
        <div>
          <div className="w-14 h-14 rounded-xl bg-brand-primary/10 flex items-center justify-center mx-auto mb-3">
            <svg className="w-7 h-7 text-brand-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
            </svg>
          </div>
          <p className="text-text-primary font-medium">Drop your resume here or click to browse</p>
          <p className="text-text-secondary text-sm mt-1">PDF only, max 5MB</p>
        </div>
      )}
    </div>
  );
}
