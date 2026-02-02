import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown'; // <--- NEU
import remarkGfm from 'remark-gfm';         // <--- NEU

const FILES = [
  "MISSION.md", "SPEC_PRODUCT.md", "SPEC_TECH.md", "PROGRESS.md", "TODO.md", "BRAINSTORM.md", "CONTEXT_AI.md"
];

function App() {
  const [activeFile, setActiveFile] = useState(FILES[0]);
  const [content, setContent] = useState("");
  const [instruction, setInstruction] = useState("");
  const [loading, setLoading] = useState(false);
  const [modelName, setModelName] = useState("");

  // --- LADE-LOGIK ---
  useEffect(() => {
    fetch(`http://127.0.0.1:8000/files/${activeFile}`)
      .then(res => res.ok ? res.json() : { content: "" })
      .then(data => setContent(data.content))
      .catch(err => setContent(""));

    fetch(`http://127.0.0.1:8000/config`)
      .then(res => res.json())
      .then(data => setModelName(data.model))
      .catch(console.error);
  }, [activeFile]);

  // --- SPEICHER-LOGIK ---
  const saveFile = async (newContent) => {
    setContent(newContent);
    try {
      await fetch(`http://127.0.0.1:8000/files/${activeFile}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: newContent })
      });
    } catch (err) { console.error(err); }
  };

  // --- KI-LOGIK ---
  const generate = async () => {
    if (!instruction.trim()) return;
    setLoading(true);
    try {
      const res = await fetch(`http://127.0.0.1:8000/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_name: activeFile, current_content: content, instruction: instruction })
      });
      const data = await res.json();
      if (data.generated) saveFile(data.generated);
    } catch (err) { alert(err.message); }
    finally { setLoading(false); setInstruction(""); }
  };

  return (
    <div className="flex h-screen bg-zinc-950 text-zinc-200 font-sans selection:bg-cyan-500/30">

      {/* SIDEBAR */}
      <div className="w-56 border-r border-zinc-800 flex flex-col bg-zinc-950 shrink-0">
        <div className="p-4">
          <h1 className="font-bold tracking-tighter text-cyan-400">AG STUDIO</h1>
        </div>
        <ul className="flex-1 overflow-y-auto px-2 space-y-1">
          {FILES.map(f => (
            <li key={f} onClick={() => setActiveFile(f)}
              className={`px-3 py-1.5 text-sm rounded cursor-pointer truncate transition-colors ${activeFile === f ? 'bg-zinc-800 text-cyan-400 font-medium' : 'text-zinc-400 hover:bg-zinc-900'}`}
            >
              {f}
            </li>
          ))}
        </ul>
      </div>

      {/* HAUPTBEREICH */}
      <div className="flex-1 flex flex-col min-w-0">

        {/* HEADER */}
        <div className="h-12 border-b border-zinc-800 flex items-center justify-between px-4 bg-zinc-950">
          <span className="font-mono text-sm text-zinc-400">{activeFile}</span>
          <span className="text-xs text-zinc-600 font-mono">{modelName}</span>
        </div>

        {/* SPLIT VIEW AREA */}
        <div className="flex-1 flex overflow-hidden">

          {/* LINKER BEREICH: EDITOR */}
          <textarea
            className="w-1/2 h-full bg-zinc-900/50 p-6 font-mono text-sm leading-relaxed text-zinc-300 resize-none outline-none border-r border-zinc-800 focus:bg-zinc-900 transition-colors"
            spellCheck="false"
            value={content}
            onChange={(e) => saveFile(e.target.value)}
          />

          {/* RECHTER BEREICH: PREVIEW */}
          <div className="w-1/2 h-full bg-zinc-950 p-8 overflow-y-auto">
            {/* 'prose' Klasse macht das Styling automatisch, 'prose-invert' für Dark Mode */}
            <div className="prose prose-invert prose-sm max-w-none prose-headings:text-cyan-100 prose-a:text-cyan-400">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {content}
              </ReactMarkdown>
            </div>
          </div>

        </div>

        {/* PROMPT BAR */}
        <div className="p-3 bg-zinc-950 border-t border-zinc-800">
          <div className="max-w-3xl mx-auto flex gap-2">
            <input
              className="flex-1 bg-zinc-900 border border-zinc-800 rounded px-3 py-2 text-sm focus:border-cyan-500/50 outline-none"
              placeholder="Anweisung an Gemini..."
              value={instruction}
              onChange={(e) => setInstruction(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && generate()}
            />
            <button
              onClick={generate}
              disabled={loading}
              className="bg-cyan-600 hover:bg-cyan-500 text-white px-4 py-2 rounded text-sm font-medium disabled:opacity-50"
            >
              {loading ? "..." : "Magic"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;