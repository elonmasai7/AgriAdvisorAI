import React, { useState } from 'react';
import UploadZone from './components/UploadZone';
import DiagnosisCard from './components/DiagnosisCard';
import ChatWindow from './components/ChatWindow';
import LanguageToggle from './components/LanguageToggle';
import { diagnose, followUp } from './api/agriApi';

function App() {
    const [currentDiagnosis, setCurrentDiagnosis] = useState(null);
    const [conversationHistory, setConversationHistory] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [language, setLanguage] = useState('en');
    const [description, setDescription] = useState('');
    const [selectedFile, setSelectedFile] = useState(null);

    const handleDiagnose = async () => {
        if (!description.trim() && !selectedFile) return;

        setIsLoading(true);
        try {
            const result = await diagnose(selectedFile, description, language);
            setCurrentDiagnosis(result);
            setConversationHistory([]); // Reset chat for new diagnosis
        } catch (error) {
            console.error('Diagnosis failed:', error);
            alert('Diagnosis failed. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleFollowUp = async (message) => {
        const newHistory = [...conversationHistory, { role: 'user', content: message }];
        setConversationHistory(newHistory);
        setIsLoading(true);

        try {
            const reply = await followUp(message, newHistory, language);
            setConversationHistory([...newHistory, { role: 'assistant', content: reply }]);
        } catch (error) {
            console.error('Follow-up failed:', error);
            alert('Follow-up failed. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleLanguageToggle = async () => {
        const newLanguage = language === 'en' ? 'sw' : 'en';
        setLanguage(newLanguage);

        if (currentDiagnosis) {
            // Re-run diagnosis with new language
            setIsLoading(true);
            try {
                const result = await diagnose(selectedFile, description, newLanguage);
                setCurrentDiagnosis(result);
                // Keep chat history but translate? For simplicity, reset
                setConversationHistory([]);
            } catch (error) {
                console.error('Language change diagnosis failed:', error);
            } finally {
                setIsLoading(false);
            }
        }
    };

    return (
        <div className="min-h-screen bg-gray-50">
            <header className="bg-green-600 text-white p-4">
                <div className="container mx-auto flex justify-between items-center">
                    <div>
                        <h1 className="text-2xl font-bold">🌾 AgriAdvisor AI</h1>
                        <p className="text-sm">AI-powered crop advisory for every farmer</p>
                    </div>
                    <LanguageToggle language={language} onToggle={handleLanguageToggle} />
                </div>
            </header>

            <main className="container mx-auto p-4">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div className="space-y-4">
                        <UploadZone onFileChange={setSelectedFile} />
                        <textarea
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            placeholder="Describe your crop problem..."
                            className="w-full border rounded p-3 h-24"
                        />
                        <button
                            onClick={handleDiagnose}
                            disabled={isLoading || (!description.trim() && !selectedFile)}
                            className="w-full bg-green-500 text-white py-2 rounded hover:bg-green-600 disabled:bg-gray-400"
                        >
                            {isLoading ? 'Diagnosing...' : 'Diagnose'}
                        </button>
                    </div>

                    <div>
                        {currentDiagnosis && (
                            <DiagnosisCard
                                diagnosis={currentDiagnosis}
                                onFollowUpClick={handleFollowUp}
                            />
                        )}
                    </div>
                </div>

                {currentDiagnosis && (
                    <div className="mt-6">
                        <h2 className="text-xl font-semibold mb-4">Follow-up Chat</h2>
                        <ChatWindow
                            history={conversationHistory}
                            onSendMessage={handleFollowUp}
                            isLoading={isLoading}
                        />
                    </div>
                )}
            </main>

            <footer className="bg-gray-800 text-white p-4 mt-8">
                <div className="container mx-auto text-center">
                    <p>Powered by Oxlo.ai | OxBuild Hackathon 2026</p>
                </div>
            </footer>
        </div>
    );
}

export default App;