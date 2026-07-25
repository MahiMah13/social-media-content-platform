import React, { useState, useEffect } from 'react';
import { Sparkles, Calendar as CalendarIcon, BarChart3, Plus, Send } from 'lucide-react';

interface Post {
  id: string;
  topic: string;
  platform: string;
  caption: string;
  hashtags: string[];
  call_to_action: string;
  scheduled_date: string;
}

interface AnalyticsData {
  total_posts: number;
  scheduled_posts: number;
  published_posts: number;
  platforms_breakdown: Record<string, number>;
  engagement_rate_avg: string;
  growth_trend: string;
}

export default function App() {
  const [activeTab, setActiveTab] = useState<'calendar' | 'generate' | 'analytics'>('calendar');
  const [loading, setLoading] = useState(false);
  const [companyName, setCompanyName] = useState('TechNova');
  const [topic, setTopic] = useState('Launch of AI Assistant');
  const [platform, setPlatform] = useState('LinkedIn');
  const [brandVoice, setBrandVoice] = useState('Professional');

  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);

  const [posts, setPosts] = useState<Post[]>([
    {
      id: '1',
      topic: 'AI Innovation Launch',
      platform: 'LinkedIn',
      caption: '🚀 Revolutionizing social media management with Generative AI! Meet our new smart scheduling engine.',
      hashtags: ['#AI', '#SaaS', '#TechInnovation'],
      call_to_action: 'Try it free today!',
      scheduled_date: '2026-07-28',
    },
  ]);

  useEffect(() => {
    if (activeTab === 'analytics') {
      fetch('http://127.0.0.1:8000/api/analytics')
        .then((res) => res.json())
        .then((data) => setAnalytics(data))
        .catch((err) => console.error('Failed to fetch analytics', err));
    }
  }, [activeTab]);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          company_name: companyName,
          topic: topic,
          platform: platform,
          brand_voice: brandVoice,
        }),
      });

      const data = await response.json();

      const newPost: Post = {
        id: Date.now().toString(),
        topic: topic,
        platform: platform,
        caption: data.caption,
        hashtags: data.hashtags || [],
        call_to_action: data.call_to_action || '',
        scheduled_date: new Date().toISOString().split('T')[0],
      };

      setPosts([newPost, ...posts]);
      setActiveTab('calendar');
    } catch (err) {
      alert('Error generating post. Ensure backend is running at http://127.0.0.1:8000');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex">
      {/* Sidebar Navigation */}
      <aside className="w-64 bg-slate-950 border-r border-slate-800 p-6 flex flex-col justify-between">
        <div>
          <div className="flex items-center gap-2 mb-8 text-indigo-400 font-bold text-xl">
            <Sparkles className="w-6 h-6" />
            <span>ContentAI</span>
          </div>

          <nav className="space-y-2">
            <button
              onClick={() => setActiveTab('calendar')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition ${
                activeTab === 'calendar' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:bg-slate-800'
              }`}
            >
              <CalendarIcon className="w-4 h-4" /> Content Calendar
            </button>
            <button
              onClick={() => setActiveTab('generate')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition ${
                activeTab === 'generate' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:bg-slate-800'
              }`}
            >
              <Sparkles className="w-4 h-4" /> AI Generator
            </button>
            <button
              onClick={() => setActiveTab('analytics')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition ${
                activeTab === 'analytics' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:bg-slate-800'
              }`}
            >
              <BarChart3 className="w-4 h-4" /> Analytics
            </button>
          </nav>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 p-8 overflow-y-auto">
        {activeTab === 'calendar' ? (
          <div>
            <div className="flex justify-between items-center mb-6">
              <div>
                <h1 className="text-2xl font-bold">Content Calendar</h1>
                <p className="text-slate-400 text-sm">Manage and schedule your social media content</p>
              </div>
              <button
                onClick={() => setActiveTab('generate')}
                className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 px-4 py-2 rounded-lg font-medium text-sm transition"
              >
                <Plus className="w-4 h-4" /> New AI Post
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {posts.map((post) => (
                <div key={post.id} className="bg-slate-800 border border-slate-700 rounded-xl p-5 flex flex-col justify-between shadow-lg">
                  <div>
                    <div className="flex justify-between items-center mb-3">
                      <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-indigo-950 text-indigo-300 border border-indigo-800">
                        {post.platform}
                      </span>
                      <span className="text-xs text-slate-400">{post.scheduled_date}</span>
                    </div>
                    <h3 className="font-semibold text-slate-200 mb-2">{post.topic}</h3>
                    <p className="text-slate-300 text-sm mb-4 line-clamp-4">{post.caption}</p>
                  </div>
                  <div>
                    <div className="flex flex-wrap gap-1 mb-3">
                      {post.hashtags.map((tag, idx) => (
                        <span key={idx} className="text-xs text-indigo-400">{tag}</span>
                      ))}
                    </div>
                    {post.call_to_action && (
                      <p className="text-xs text-emerald-400 font-medium italic">CTA: {post.call_to_action}</p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : activeTab === 'generate' ? (
          <div className="max-w-2xl mx-auto bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-xl">
            <h1 className="text-2xl font-bold mb-1 flex items-center gap-2">
              <Sparkles className="w-6 h-6 text-indigo-400" /> Generate Social Post
            </h1>
            <p className="text-slate-400 text-sm mb-6">Powered by Google Gemini 2.5 Flash</p>

            <form onSubmit={handleGenerate} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">Company Name</label>
                <input
                  type="text"
                  value={companyName}
                  onChange={(e) => setCompanyName(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-indigo-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">Topic / Post Goal</label>
                <input
                  type="text"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-indigo-500"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Platform</label>
                  <select
                    value={platform}
                    onChange={(e) => setPlatform(e.target.value)}
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-indigo-500"
                  >
                    <option>LinkedIn</option>
                    <option>Twitter/X</option>
                    <option>Instagram</option>
                    <option>Facebook</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Brand Voice</label>
                  <select
                    value={brandVoice}
                    onChange={(e) => setBrandVoice(e.target.value)}
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-indigo-500"
                  >
                    <option>Professional</option>
                    <option>Casual & Friendly</option>
                    <option>Energetic & Bold</option>
                    <option>Informative</option>
                  </select>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-2.5 rounded-lg transition flex items-center justify-center gap-2 mt-4"
              >
                {loading ? 'Generating with Gemini...' : <><Send className="w-4 h-4" /> Generate Post</>}
              </button>
            </form>
          </div>
        ) : (
          <div>
            <h1 className="text-2xl font-bold mb-1">Platform Analytics</h1>
            <p className="text-slate-400 text-sm mb-6">Track engagement and performance across your channels</p>

            {analytics ? (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-lg">
                  <h3 className="text-slate-400 text-sm font-medium mb-2">Total Posts</h3>
                  <p className="text-3xl font-bold text-indigo-400">{analytics.total_posts}</p>
                </div>
                <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-lg">
                  <h3 className="text-slate-400 text-sm font-medium mb-2">Avg Engagement Rate</h3>
                  <p className="text-3xl font-bold text-emerald-400">{analytics.engagement_rate_avg}</p>
                </div>
                <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-lg">
                  <h3 className="text-slate-400 text-sm font-medium mb-2">Growth Trend</h3>
                  <p className="text-3xl font-bold text-sky-400">{analytics.growth_trend}</p>
                </div>
              </div>
            ) : (
              <p className="text-slate-400">Loading analytics...</p>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
