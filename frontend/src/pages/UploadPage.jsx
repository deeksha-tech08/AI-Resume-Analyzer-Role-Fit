/**
 * UploadPage — resume upload with ATS score preview.
 */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import FileUpload from '../components/resume/FileUpload';
import UploadProgress from '../components/resume/UploadProgress';
import UploadStatus from '../components/resume/UploadStatus';
import Button from '../components/common/Button';
import resumeService from '../services/resumeService';

export default function UploadPage() {
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [stage, setStage] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleUpload = async () => {
    if (!selectedFile) return;
    setUploading(true);
    setError('');
    setStage('uploading');

    try {
      setStage('extracting');
      const response = await resumeService.upload(selectedFile);
      setStage('analyzing');

      if (response?.success) {
        setStage('done');
        setResult(response.data);
      } else {
        throw new Error(response?.error || 'Upload failed');
      }
    } catch (err) {
      setError(err.message || 'Failed to upload resume');
      setStage('');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="flex-1 py-8 px-4 max-w-2xl mx-auto w-full">
      <div className="text-center mb-8 slide-up">
        <h1 className="text-3xl font-bold gradient-text mb-2">Upload Your Resume</h1>
        <p className="text-text-secondary">Upload a PDF resume to get your ATS score and skill analysis</p>
      </div>

      {!result && (
        <>
          <FileUpload onFileSelect={setSelectedFile} disabled={uploading} />

          {selectedFile && !uploading && (
            <div className="mt-6 text-center slide-up">
              <Button onClick={handleUpload} loading={uploading} size="lg">
                Analyze Resume
              </Button>
            </div>
          )}

          {uploading && (
            <div className="mt-6">
              <UploadProgress stage={stage} />
            </div>
          )}
        </>
      )}

      {(result || error) && (
        <div className="mt-6">
          <UploadStatus result={result} error={error} />
        </div>
      )}

      {result && (
        <div className="mt-6 text-center slide-up">
          <Button onClick={() => navigate('/roles', { state: { resumeId: result.id } })} size="lg">
            Select Roles to Analyze →
          </Button>
          <p className="text-text-secondary text-sm mt-3">
            Or <button onClick={() => { setResult(null); setSelectedFile(null); setStage(''); }} className="text-brand-primary hover:underline">upload another resume</button>
          </p>
        </div>
      )}

      {error && (
        <div className="mt-4 text-center">
          <Button variant="secondary" onClick={() => { setError(''); setSelectedFile(null); setStage(''); }}>
            Try Again
          </Button>
        </div>
      )}
    </div>
  );
}
