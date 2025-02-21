import React, { useState, useEffect } from 'react';
import MessageList from './MessageList';
import Sidebar from './Sidebar';

// Mock data for testing
const mockMessages = [
  {
    id: 1,
    title: "Neue KI-Entwicklungen im Bereich Machine Learning",
    content: "Forscher haben bahnbrechende Fortschritte im Bereich des maschinellen Lernens erzielt. Die neue Technologie ermöglicht es KI-Systemen, komplexe Aufgaben mit deutlich höherer Präzision zu bewältigen.",
    created_at: "2024-02-20T10:00:00Z",
    tags: ["KI", "Technologie", "Forschung"]
  },
  {
    id: 2,
    title: "Cybersicherheit im Fokus",
    content: "Experten warnen vor zunehmenden Cyberangriffen auf Unternehmensinfrastrukturen. Neue Sicherheitsprotokolle werden empfohlen, um sensible Daten besser zu schützen.",
    created_at: "2024-02-19T15:30:00Z",
    tags: ["Cybersecurity", "IT-Sicherheit", "Datenschutz"]
  },
  {
    id: 3,
    title: "Cloud Computing Trends 2024",
    content: "Die neuesten Entwicklungen im Cloud Computing versprechen verbesserte Skalierbarkeit und Kosteneffizienz. Unternehmen setzen verstärkt auf hybride Cloud-Lösungen.",
    created_at: "2024-02-18T09:15:00Z",
    tags: ["Cloud", "Innovation", "Business"]
  },
  {
    id: 4,
    title: "Nachhaltigkeit in der IT",
    content: "Green IT gewinnt an Bedeutung: Unternehmen implementieren zunehmend umweltfreundliche Technologielösungen und optimieren ihre Rechenzentren für bessere Energieeffizienz.",
    created_at: "2024-02-17T14:45:00Z",
    tags: ["Nachhaltigkeit", "Green IT", "Umwelt"]
  }
];

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading delay for better UX
    const timer = setTimeout(() => {
      setMessages(mockMessages);
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      <main className="flex-1 overflow-auto">
        <div className="container mx-auto px-4 py-8">
          <header className="mb-8">
            <h1 className="text-4xl font-bold text-gray-900">InfoSphere</h1>
            <p className="text-gray-600">Your Information Hub</p>
          </header>
          
          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            </div>
          ) : (
            <MessageList messages={messages} />
          )}
        </div>
      </main>
    </div>
  );
}

export default App; 