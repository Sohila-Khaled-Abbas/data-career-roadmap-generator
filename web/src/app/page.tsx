"use client"

import { useState, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export default function Home() {
  const [profiles, setProfiles] = useState<string[]>([]);
  const [selectedProfile, setSelectedProfile] = useState<string>('');
  const [skills, setSkills] = useState<any[]>([]);
  const [roadmap, setRoadmap] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    // Fetch profiles
    axios.get(`${API_BASE}/profiles`).then(res => {
      setProfiles(res.data);
      if (res.data.length > 0) setSelectedProfile(res.data[0]);
    }).catch(err => console.error("Error fetching profiles:", err));
  }, []);

  useEffect(() => {
    if (!selectedProfile) return;
    
    // Fetch top skills
    axios.get(`${API_BASE}/skills/${selectedProfile}/top?limit=15`).then(res => {
      setSkills(res.data);
    }).catch(err => console.error("Error fetching skills:", err));

    // Try to fetch pre-generated roadmap
    axios.get(`${API_BASE}/roadmaps/${selectedProfile}`).then(res => {
      setRoadmap(res.data.markdown);
    }).catch(err => {
      console.log("No saved roadmap found for this profile.");
      setRoadmap('');
    });
  }, [selectedProfile]);

  const generateRoadmap = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/roadmaps/generate`, {
        profile: selectedProfile,
        skills: skills.map(s => s.skill)
      });
      setRoadmap(res.data.markdown);
    } catch (err: any) {
      console.error("Error generating roadmap:", err);
      const detail = err.response?.data?.detail || err.message;
      alert(`Failed to generate roadmap: ${detail}\n\nPlease ensure your GEMINI_API_KEY is correct in the .env file and restart Docker.`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px' }}>
      
      {/* Brand Header */}
      <header style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '40px', borderBottom: '1px solid var(--border-color)', paddingBottom: '20px' }}>
        <div style={{ width: '50px', height: '50px', backgroundColor: 'var(--primary)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyItems: 'center', overflow: 'hidden' }}>
          <img src="/logo.png" alt="Logo" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        </div>
        <div>
          <h1 style={{ margin: 0, fontSize: '1.8rem', letterSpacing: '-0.5px' }}>The Data <span style={{ color: 'var(--primary)' }}>Tea</span></h1>
          <p style={{ margin: 0, color: '#94a3b8', fontSize: '0.9rem' }}>Steeping market insights into your career roadmap</p>
        </div>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '40px' }}>
        
        {/* Sidebar / Controls */}
        <div className="card" style={{ height: 'fit-content' }}>
          <h2 style={{ marginTop: 0 }}>Configure</h2>
          
          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px', color: '#94a3b8' }}>Target Profile</label>
            <select 
              value={selectedProfile} 
              onChange={e => setSelectedProfile(e.target.value)}
              style={{ width: '100%', padding: '10px', backgroundColor: '#334155', color: 'white', border: '1px solid #475569', borderRadius: '6px' }}
            >
              {profiles.map(p => <option key={p} value={p}>{p}</option>)}
            </select>
          </div>

          <button className="btn" style={{ width: '100%', fontWeight: 'bold' }} onClick={generateRoadmap} disabled={loading || skills.length === 0}>
            {loading ? 'Brewing your path...' : 'Generate Roadmap'}
          </button>
        </div>

        {/* Main Content Area */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '40px' }}>
          
          {/* Charts Section */}
          <div className="card">
            <h2 style={{ marginTop: 0, color: 'var(--text-color)' }}>Top In-Demand Skills</h2>
            {skills.length > 0 ? (
              <div style={{ width: '100%', height: '400px' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={skills} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                    <XAxis type="number" />
                    <YAxis dataKey="skill" type="category" width={100} stroke="#94a3b8" />
                    <Tooltip cursor={{fill: '#334155'}} contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: 'white' }} />
                    <Bar dataKey="frequency" fill="var(--primary)" radius={[0, 4, 4, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <p style={{color: '#94a3b8'}}>No skill data available. Please select a profile or run the ETL pipeline.</p>
            )}
          </div>

          {/* Roadmap Display Section */}
          {roadmap && (
            <div className="card" style={{ borderLeft: '4px solid var(--primary)' }}>
              <h2 style={{ marginTop: 0, color: 'var(--primary)' }}>Your Learning Roadmap</h2>
              <div style={{ lineHeight: '1.6' }}>
                <ReactMarkdown>{roadmap}</ReactMarkdown>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}
