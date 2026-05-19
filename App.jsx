import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, Send, X, Settings, Terminal, CheckCircle, Brain } from 'lucide-react';

export default function App() {
  const [messages, setMessages] = useState([
    { id: 1, role: 'assistant', text: 'Hello! I am your AI Desktop Assistant. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [isListening, setIsListening] = useState(false);
  
  // Fake Electron IPC logic (if available in window)
  const closeWindow = () => {
    if (window.require) {
      const { ipcRenderer } = window.require('electron');
      ipcRenderer.send('window-close');
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMsg = { id: Date.now(), role: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');

    // Call local FastAPI backend
    try {
      const res = await fetch('http://127.0.0.1:8080/api/v1/chat', { // using 8080 as set earlier
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg.text })
      });
      
      // If we don't have the real endpoint yet, just mock it
      if (!res.ok) throw new Error('API not implemented fully');
      
      const data = await res.json();
      setMessages(prev => [...prev, { id: Date.now(), role: 'assistant', text: data.message }]);
      
    } catch (e) {
      setTimeout(() => {
        setMessages(prev => [...prev, { 
          id: Date.now(), 
          role: 'assistant', 
          text: `Processing task: "${userMsg.text}". (Backend endpoint under construction)`
        }]);
      }, 800);
    }
  };

  return (
    <div className="w-full h-full p-4">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full h-full rounded-2xl overflow-hidden flex flex-col bg-gray-950/80 backdrop-blur-2xl border border-white/10 shadow-[0_0_50px_rgba(0,0,0,0.5)]"
      >
        {/* Header - Draggable */}
        <div className="drag-region h-14 bg-white/5 border-b border-white/10 flex items-center justify-between px-4 shrink-0">
          <div className="flex items-center gap-2 text-white/90 font-medium">
            <Brain className="w-5 h-5 text-indigo-400" />
            <span>AI Assistant</span>
          </div>
          <div className="flex items-center gap-3 no-drag">
            <button className="text-white/50 hover:text-white transition-colors">
              <Settings className="w-4 h-4" />
            </button>
            <button onClick={closeWindow} className="text-white/50 hover:text-red-400 transition-colors">
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-4 no-scrollbar">
          <AnimatePresence>
            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, scale: 0.9, y: 10 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                className={`max-w-[85%] rounded-2xl p-3 ${
                  msg.role === 'user' 
                    ? 'bg-indigo-600/80 text-white self-end rounded-tr-sm' 
                    : 'bg-white/10 text-white/90 self-start rounded-tl-sm border border-white/5'
                }`}
              >
                <p className="text-sm leading-relaxed">{msg.text}</p>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>

        {/* Status Bar */}
        <div className="px-4 py-2 bg-black/40 border-t border-white/5 flex items-center justify-between text-[11px] text-white/40">
          <div className="flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
            System Online
          </div>
          <div>Port: 8080</div>
        </div>

        {/* Input Area */}
        <div className="p-3 bg-white/5 shrink-0 no-drag">
          <div className="relative flex items-center bg-black/50 border border-white/10 rounded-xl overflow-hidden focus-within:border-indigo-500/50 transition-colors">
            <button 
              onClick={() => setIsListening(!isListening)}
              className={`p-3 transition-colors ${isListening ? 'text-rose-400' : 'text-white/50 hover:text-white/80'}`}
            >
              <Mic className="w-5 h-5" />
            </button>
            <input 
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask me to do anything..."
              className="flex-1 bg-transparent border-none outline-none text-white text-sm placeholder:text-white/30"
            />
            <button 
              onClick={handleSend}
              className="p-3 text-indigo-400 hover:text-indigo-300 transition-colors disabled:opacity-50"
              disabled={!input.trim()}
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
