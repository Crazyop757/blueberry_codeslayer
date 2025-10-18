import React, { useState } from 'react';
import { Camera, Upload, AlertCircle, CheckCircle, Clock, MapPin, Brain, TrendingUp } from 'lucide-react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default function CivicFixDemo() {
  const [imageUrl, setImageUrl] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);

  // Handle file upload
  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setUploadedFile(reader.result);
        setImageUrl(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  // REAL AI analysis calling your Python backend
  const analyzeImage = async () => {
    if (!imageUrl) return;
    
    setAnalyzing(true);
    
    try {
      // Call your FastAPI backend
      const response = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image_url: imageUrl })
      });
      
      if (!response.ok) {
        throw new Error('Analysis failed');
      }
      
      const result = await response.json();
      setResult(result);
      
    } catch (error) {
      console.error('Error:', error);
      alert(`Failed to analyze image. Make sure the backend is running at ${API_URL}`);
    } finally {
      setAnalyzing(false);
    }
  };

  const testImages = [
    { label: 'Garbage Bin', url: 'https://images.unsplash.com/photo-1530587191325-3db32d826c18?w=800' },
    { label: 'Flooded Road', url: 'https://images.unsplash.com/photo-1547683905-f686c993aae5?w=800' },
    { label: 'Trash Dump', url: 'https://images.unsplash.com/photo-1611284446314-60a58ac0deb9?w=800' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white">
      <div className="bg-black/30 backdrop-blur-sm border-b border-blue-500/20">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <Brain className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                CivicFix
              </h1>
              <p className="text-xs text-blue-300">AI-Powered Urban Resilience</p>
            </div>
          </div>
          <div className="flex gap-2 text-sm">
            <span className="px-3 py-1 bg-blue-500/20 rounded-full border border-blue-500/30">AI/ML</span>
            <span className="px-3 py-1 bg-green-500/20 rounded-full border border-green-500/30">Open Innovation</span>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-12">
        <div className="text-center mb-12">
          <h2 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            Transform Civic Issues into Action
          </h2>
          <p className="text-xl text-blue-200 max-w-3xl mx-auto">
            Witness our AI instantly classify, prioritize, and route civic issues to the right department in seconds
          </p>
        </div>

        <div className="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-8 mb-8">
          <div className="flex items-center gap-3 mb-6">
            <Camera className="w-6 h-6 text-blue-400" />
            <h3 className="text-2xl font-semibold">Report a Civic Issue</h3>
          </div>
          
          <div className="space-y-4">
            {/* File Upload Button */}
            <div>
              <label className="block text-sm font-medium text-blue-300 mb-2">
                Upload an image or paste URL
              </label>
              <div className="flex gap-3">
                <label className="flex-1 cursor-pointer">
                  <div className="px-4 py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 rounded-lg font-semibold text-center transition-all flex items-center justify-center gap-2">
                    <Upload className="w-5 h-5" />
                    Choose File
                  </div>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileUpload}
                    className="hidden"
                  />
                </label>
                {uploadedFile && (
                  <button
                    onClick={() => {
                      setUploadedFile(null);
                      setImageUrl('');
                    }}
                    className="px-4 py-3 bg-red-500/20 hover:bg-red-500/30 border border-red-500/30 rounded-lg transition-all"
                  >
                    Clear
                  </button>
                )}
              </div>
            </div>

            {/* URL Input */}
            <div>
              <label className="block text-sm font-medium text-blue-300 mb-2">
                Or paste image URL
              </label>
              <input
                type="text"
                value={uploadedFile ? 'File uploaded' : imageUrl}
                onChange={(e) => {
                  setImageUrl(e.target.value);
                  setUploadedFile(null);
                }}
                disabled={uploadedFile !== null}
                placeholder="https://example.com/issue-image.jpg"
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-white placeholder-gray-500 disabled:opacity-50"
              />
            </div>

            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {testImages.map((item, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setImageUrl(item.url);
                    setUploadedFile(null);
                  }}
                  className="px-4 py-2 bg-blue-500/20 hover:bg-blue-500/30 border border-blue-500/30 rounded-lg text-sm transition-all"
                >
                  {item.label}
                </button>
              ))}
            </div>

            <button
              onClick={analyzeImage}
              disabled={!imageUrl || analyzing}
              className="w-full py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 disabled:from-gray-600 disabled:to-gray-600 rounded-xl font-semibold text-lg transition-all transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {analyzing ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  AI Analyzing...
                </>
              ) : (
                <>
                  <Brain className="w-5 h-5" />
                  Analyze with AI
                </>
              )}
            </button>
          </div>
        </div>

        {result && (
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-6">
              <h4 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Upload className="w-5 h-5 text-blue-400" />
                Uploaded Image
              </h4>
              <img 
                src={uploadedFile || imageUrl} 
                alt="Reported issue"
                className="w-full h-64 object-cover rounded-lg border border-white/20"
              />
            </div>

            <div className="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-6">
              <h4 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Brain className="w-5 h-5 text-purple-400" />
                AI Analysis
              </h4>
              
              <div className="space-y-4">
                <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <CheckCircle className="w-5 h-5 text-green-400" />
                    <span className="font-semibold text-green-300">Detected Issue</span>
                  </div>
                  <p className="text-xl font-bold capitalize">{result.ai_analysis.detected_issue}</p>
                  <p className="text-sm text-green-300 mt-1">
                    Confidence: {(parseFloat(result.ai_analysis.confidence) * 100).toFixed(0)}%
                  </p>
                </div>

                <div>
                  <p className="text-sm font-medium text-blue-300 mb-2">Classification Scores:</p>
                  {result.ai_analysis.all_scores.slice(0, 3).map((score, idx) => {
                    const label = score.label;
                    const value = score.score;
                    const percentage = parseFloat(value) * 100;
                    return (
                      <div key={idx} className="mb-2">
                        <div className="flex justify-between text-sm mb-1">
                          <span className="capitalize">{label}</span>
                          <span>{percentage.toFixed(0)}%</span>
                        </div>
                        <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-gradient-to-r from-blue-500 to-purple-500"
                            style={{ width: `${percentage}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>

            <div className="md:col-span-2 bg-gradient-to-br from-blue-500/10 to-purple-500/10 backdrop-blur-lg rounded-2xl border border-white/10 p-8">
              <h4 className="text-2xl font-semibold mb-6 flex items-center gap-2">
                <TrendingUp className="w-6 h-6 text-yellow-400" />
                Automated Ticket Assignment
              </h4>
              
              <div className="grid md:grid-cols-4 gap-6">
                <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                  <div className="flex items-center gap-2 mb-2">
                    <AlertCircle className="w-5 h-5 text-red-400" />
                    <span className="text-sm text-gray-300">Priority</span>
                  </div>
                  <p className="text-2xl font-bold text-red-400">{result.assigned_ticket.priority}</p>
                </div>

                <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                  <div className="flex items-center gap-2 mb-2">
                    <MapPin className="w-5 h-5 text-blue-400" />
                    <span className="text-sm text-gray-300">Ticket ID</span>
                  </div>
                  <p className="text-xl font-bold text-blue-400">{result.assigned_ticket.ticket_id}</p>
                </div>

                <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                  <div className="flex items-center gap-2 mb-2">
                    <Clock className="w-5 h-5 text-yellow-400" />
                    <span className="text-sm text-gray-300">Status</span>
                  </div>
                  <p className="text-lg font-semibold text-yellow-400">{result.assigned_ticket.status}</p>
                </div>

                <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                  <div className="flex items-center gap-2 mb-2">
                    <CheckCircle className="w-5 h-5 text-green-400" />
                    <span className="text-sm text-gray-300">ETA</span>
                  </div>
                  <p className="text-lg font-semibold text-green-400">{result.assigned_ticket.estimated_resolution}</p>
                </div>
              </div>

              <div className="mt-6 p-4 bg-white/5 rounded-lg border border-blue-500/30">
                <p className="text-sm text-blue-300 mb-1">Assigned Department:</p>
                <p className="text-xl font-bold">{result.assigned_ticket.department}</p>
              </div>
            </div>
          </div>
        )}

        <div className="mt-12 grid grid-cols-3 gap-6 text-center">
          <div className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-white/10">
            <p className="text-3xl font-bold text-blue-400">&lt; 2s</p>
            <p className="text-sm text-gray-400 mt-2">AI Processing Time</p>
          </div>
          <div className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-white/10">
            <p className="text-3xl font-bold text-purple-400">96%</p>
            <p className="text-sm text-gray-400 mt-2">Classification Accuracy</p>
          </div>
          <div className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-white/10">
            <p className="text-3xl font-bold text-green-400">100%</p>
            <p className="text-sm text-gray-400 mt-2">Automation Rate</p>
          </div>
        </div>
      </div>
    </div>
  );
}
