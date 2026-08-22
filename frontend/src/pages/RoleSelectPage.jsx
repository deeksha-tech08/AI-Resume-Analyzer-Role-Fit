/**
 * RoleSelectPage — select 1-4 roles and run analysis.
 */
import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Button from '../components/common/Button';
import ErrorMessage from '../components/common/ErrorMessage';
import useAnalysis from '../hooks/useAnalysis';
import resumeService from '../services/resumeService';

const AVAILABLE_ROLES = [
  { name: 'Software Engineer', icon: '💻', desc: 'Full-stack development with CS fundamentals' },
  { name: 'SDE', icon: '🧑‍💻', desc: 'Software Development Engineer, Data Structures, Algorithms' },
  { name: 'Backend Developer', icon: '⚙️', desc: 'Server-side APIs, databases, infrastructure' },
  { name: 'Data Analyst', icon: '📊', desc: 'Data analysis, SQL, visualization' },
  { name: 'AI/ML Engineer', icon: '🤖', desc: 'Machine learning, model development' },
  { name: 'DevOps Engineer', icon: '♾️', desc: 'Infrastructure, CI/CD, cloud deployment' },
  { name: 'QA Engineer', icon: '🧪', desc: 'Quality assurance, test automation' },
  { name: 'Full Stack Developer', icon: '🌐', desc: 'End-to-end web application development' },
  { name: 'Cloud Architect', icon: '☁️', desc: 'Cloud infrastructure design and scalable architecture' },
  { name: 'Mobile Developer', icon: '📱', desc: 'Cross-platform and native mobile apps' },
  { name: 'Security Engineer', icon: '🛡️', desc: 'System security, penetration testing' },
  { name: 'Frontend Developer', icon: '🎨', desc: 'User interface design and implementation' },
  { name: 'Data Scientist', icon: '🔬', desc: 'Predictive modeling and advanced analytics' },
  { name: 'React Developer', icon: '⚛️', desc: 'Frontend development using React' },
  { name: 'Python Developer', icon: '🐍', desc: 'Python-based application development' },
  { name: 'Java Developer', icon: '☕', desc: 'Enterprise software development' },
  { name: 'Database Administrator', icon: '🗄️', desc: 'Database management and optimization' },
  { name: 'Infrastructure Engineer', icon: '🏗️', desc: 'Systems and infrastructure management' },
  { name: 'Platform Engineer', icon: '🛠️', desc: 'Internal developer platform building' },
  { name: 'Site Reliability Engineer (SRE)', icon: '🚨', desc: 'System reliability and performance' },
  { name: 'Cloud Engineer', icon: '🌩️', desc: 'Cloud deployment and maintenance' },
  { name: 'Solutions Architect', icon: '📐', desc: 'Designing technical solutions' },
  { name: 'MLOps Engineer', icon: '🔄', desc: 'Deploying and maintaining ML models' },
  { name: 'Technical Lead / Engineering Manager', icon: '👥', desc: 'Team leadership and technical direction' },
  { name: 'Embedded Systems Engineer', icon: '🔌', desc: 'Hardware and low-level software' },
  { name: 'Game Developer', icon: '🎮', desc: 'Video game development' },
  { name: 'Blockchain Developer', icon: '⛓️', desc: 'Decentralized application development' },
  { name: 'Product Manager (Tech)', icon: '📈', desc: 'Technical product strategy' },
  { name: 'Growth Engineer', icon: '🚀', desc: 'Engineering for user acquisition' },
  { name: 'Staff Engineer / Principal Engineer', icon: '🏛️', desc: 'High-level technical leadership' }
];

export default function RoleSelectPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { runAnalysis, loading, error, setError } = useAnalysis();
  const [selectedRoles, setSelectedRoles] = useState([]);
  const [resumeId, setResumeId] = useState(location.state?.resumeId || '');
  const [resumeInfo, setResumeInfo] = useState(null);

  // If no resumeId passed, fetch latest resume
  useEffect(() => {
    if (!resumeId) {
      resumeService.getLatest().then(res => {
        if (res?.success && res.data) {
          setResumeId(res.data.id);
          setResumeInfo(res.data);
        }
      }).catch(() => {
        setError('No resume found. Please upload a resume first.');
      });
    }
  }, [resumeId, setError]);

  const toggleRole = (roleName) => {
    setSelectedRoles(prev => {
      if (prev.includes(roleName)) {
        return prev.filter(r => r !== roleName);
      }
      if (prev.length >= 4) return prev;
      return [...prev, roleName];
    });
  };

  const handleAnalyze = async () => {
    if (!resumeId || selectedRoles.length === 0) return;
    try {
      const result = await runAnalysis(resumeId, selectedRoles);
      if (result?.id) {
        navigate(`/results/${result.id}`);
      }
    } catch {
      // Error is set by the hook
    }
  };

  const handleDiscover = async () => {
    if (!resumeId) return;
    try {
      const allRoles = AVAILABLE_ROLES.map(r => r.name);
      const result = await runAnalysis(resumeId, allRoles);
      if (result?.id) {
        navigate(`/results/${result.id}`);
      }
    } catch {
      // Error is set by the hook
    }
  };

  return (
    <div className="flex-1 py-8 px-4 max-w-3xl mx-auto w-full">
      <div className="text-center mb-8 slide-up">
        <h1 className="text-3xl font-bold gradient-text mb-2">Select Target Roles</h1>
        <p className="text-text-secondary">
          Choose 1-4 roles to analyze your resume against
        </p>
      </div>

      {resumeInfo && (
        <div className="glass-card p-4 mb-6 flex items-center justify-between slide-up">
          <div>
            <p className="text-sm text-text-secondary">Analyzing resume:</p>
            <p className="text-text-primary font-medium">{resumeInfo.filename}</p>
          </div>
          <span className="text-brand-primary font-bold">{resumeInfo.ats_score}% ATS</span>
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
        {AVAILABLE_ROLES.map((role) => {
          const isSelected = selectedRoles.includes(role.name);
          return (
            <button
              key={role.name}
              onClick={() => toggleRole(role.name)}
              disabled={loading}
              className={`glass-card p-5 text-left transition-all duration-200 ${
                isSelected ? 'best-fit-glow ring-1 ring-brand-primary' : 'hover:bg-white/[0.04]'
              }`}
            >
              <div className="flex items-center gap-3 mb-2">
                <span className="text-2xl">{role.icon}</span>
                <h3 className="text-lg font-semibold text-text-primary">{role.name}</h3>
              </div>
              <p className="text-text-secondary text-sm">{role.desc}</p>
              {isSelected && (
                <div className="mt-2 flex items-center gap-1 text-brand-primary text-xs font-medium">
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                  Selected
                </div>
              )}
            </button>
          );
        })}
      </div>

      {error && <ErrorMessage message={error} onRetry={() => setError('')} />}

      <div className="text-center slide-up">
        <p className="text-text-secondary text-sm mb-4">
          {selectedRoles.length}/4 roles selected manually
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Button
            onClick={handleAnalyze}
            loading={loading}
            disabled={selectedRoles.length === 0 || !resumeId}
            size="lg"
          >
            {loading ? 'Analyzing...' : `Analyze Against ${selectedRoles.length} Role${selectedRoles.length !== 1 ? 's' : ''}`}
          </Button>
          <div className="text-text-secondary text-sm font-medium">OR</div>
          <Button
            onClick={handleDiscover}
            loading={loading}
            disabled={!resumeId}
            size="lg"
            className="bg-gradient-to-r from-accent-emerald to-accent-cyan"
          >
            ✨ Discover My Best Roles
          </Button>
        </div>
      </div>
    </div>
  );
}
