"use client"

import { useState, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

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
    <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '40px 20px' }}>
      
      {/* Brand Header */}
      <header className="animate-fade-in" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: '15px', marginBottom: '60px', textAlign: 'center' }}>
        <div style={{ width: '80px', height: '80px', backgroundColor: 'var(--card-bg)', border: '1px solid var(--primary)', borderRadius: '20px', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden', boxShadow: '0 0 30px var(--primary-glow)' }}>
          <img src="/logo.png" alt="Logo" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        </div>
        <div>
          <h1 style={{ margin: 0, fontSize: '3rem', letterSpacing: '-1px' }}>The Data <span className="gradient-text">Tea</span></h1>
          <p style={{ margin: '10px 0 0 0', color: 'var(--text-muted)', fontSize: '1.1rem', maxWidth: '500px' }}>Steeping real-time market insights into your personalized data career roadmap.</p>
        </div>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2.5fr', gap: '40px', alignItems: 'start' }}>
        
        {/* Sidebar / Controls */}
        <div className="card animate-fade-in delay-100" style={{ position: 'sticky', top: '40px' }}>
          <h2 style={{ marginTop: 0, marginBottom: '24px', fontSize: '1.5rem' }}>Configuration</h2>
          
          <div style={{ marginBottom: '30px' }}>
            <label style={{ display: 'block', marginBottom: '10px', color: 'var(--text-muted)', fontWeight: 500 }}>Target Role</label>
            <div className="custom-select-wrapper">
              <select 
                className="custom-select"
                value={selectedProfile} 
                onChange={e => setSelectedProfile(e.target.value)}
              >
                {profiles.map(p => <option key={p} value={p}>{p}</option>)}
              </select>
              <div className="select-arrow">▼</div>
            </div>
          </div>

          <button className="btn" style={{ width: '100%' }} onClick={generateRoadmap} disabled={loading || skills.length === 0}>
            {loading ? (
              <span style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px'}}>
                <span className="spinner" style={{width: '20px', height: '20px', border: '3px solid rgba(255,255,255,0.3)', borderTop: '3px solid white', borderRadius: '50%', animation: 'spin 1s linear infinite'}} />
                Brewing Roadmap...
              </span>
            ) : 'Generate Custom Roadmap'}
          </button>
          
          <style dangerouslySetInnerHTML={{__html: `
            @keyframes spin { 100% { transform: rotate(360deg); } }
          `}} />
        </div>

        {/* Main Content Area */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '40px' }}>
          
          {/* Charts Section */}
          <div className="card animate-fade-in delay-200">
            <h2 style={{ marginTop: 0, marginBottom: '24px', color: 'var(--text-color)', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{color: 'var(--primary)'}}>⚡</span> Top In-Demand Skills
            </h2>
            {skills.length > 0 ? (
              <div style={{ width: '100%', height: '450px' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={skills} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                    <XAxis type="number" hide />
                    <YAxis dataKey="skill" type="category" width={120} stroke="var(--text-muted)" axisLine={false} tickLine={false} tick={{fill: 'var(--text-color)', fontSize: 14, fontFamily: 'Outfit'}} />
                    <Tooltip 
                      cursor={{fill: 'rgba(255,255,255,0.05)'}} 
                      contentStyle={{ backgroundColor: 'var(--card-bg)', backdropFilter: 'blur(10px)', border: '1px solid var(--card-border)', borderRadius: '12px', color: 'white', fontFamily: 'Outfit' }} 
                      itemStyle={{color: 'var(--primary)'}}
                    />
                    <Bar dataKey="frequency" radius={[0, 8, 8, 0]} barSize={24}>
                      {skills.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={`rgba(16, 185, 129, ${1 - index * 0.05})`} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <div style={{padding: '40px', textAlign: 'center', color: 'var(--text-muted)', background: 'rgba(0,0,0,0.2)', borderRadius: '12px'}}>
                <p>No skill data available. Please select a profile or run the ETL pipeline.</p>
              </div>
            )}
          </div>

          {/* Roadmap Display Section */}
          {roadmap && (
            <div className="card animate-fade-in delay-300" style={{ borderTop: '4px solid var(--primary)', position: 'relative' }}>
              <div style={{position: 'absolute', top: 0, left: '50%', transform: 'translateX(-50%)', width: '100px', height: '4px', background: 'var(--primary)', boxShadow: '0 0 20px var(--primary)'}}></div>
              <h2 style={{ marginTop: 0, marginBottom: '30px', color: 'white', display: 'flex', alignItems: 'center', gap: '10px', fontSize: '1.8rem' }}>
                <span className="gradient-text">Your Learning Roadmap</span> 🚀
              </h2>
              <div className="markdown-body" style={{ lineHeight: '1.8', fontSize: '1.05rem' }}>
                <ReactMarkdown>{roadmap}</ReactMarkdown>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}
