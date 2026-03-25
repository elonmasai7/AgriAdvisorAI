import { useMemo, useState } from "react";

import { diagnose, followUp } from "./api/agriApi";
import ChatWindow from "./components/ChatWindow";
import DiagnosisCard from "./components/DiagnosisCard";
import LanguageToggle from "./components/LanguageToggle";
import UploadZone from "./components/UploadZone";

export default function App() {
  const [currentDiagnosis, setCurrentDiagnosis] = useState(null);
  const [conversationHistory, setConversationHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [language, setLanguage] = useState("en");
  const [activeTab, setActiveTab] = useState("diagnose");

  const [description, setDescription] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);

  const canDiagnose = useMemo(() => Boolean(description.trim() || selectedFile), [description, selectedFile]);

  const runDiagnosis = async (targetLanguage) => {
    if (!description.trim() && !selectedFile) return;

    setIsLoading(true);
    try {
      const result = await diagnose(selectedFile, description, targetLanguage);
      setCurrentDiagnosis(result);
      setConversationHistory([]);
      setActiveTab("diagnose");
    } catch (error) {
      console.error("Diagnosis failed:", error);
      window.alert("Diagnosis failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDiagnose = async () => {
    await runDiagnosis(language);
  };

  const handleLanguageToggle = async (targetLanguage) => {
    if (targetLanguage === language) return;

    setLanguage(targetLanguage);
    if (currentDiagnosis) {
      await runDiagnosis(targetLanguage);
    }
  };

  const handleFollowup = async (message) => {
    const nextHistory = [...conversationHistory, { role: "user", content: message }];
    setConversationHistory(nextHistory);
    setActiveTab("chat");
    setIsLoading(true);

    try {
      const reply = await followUp(message, nextHistory, language, currentDiagnosis);
      setConversationHistory([...nextHistory, { role: "assistant", content: reply }]);
    } catch (error) {
      console.error("Follow-up failed:", error);
      window.alert("Follow-up failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <header className="border-b bg-green-600 text-white">
        <div className="mx-auto flex w-full max-w-6xl flex-wrap items-center justify-between gap-3 px-4 py-4">
          <div>
            <h1 className="text-2xl font-bold">?? AgriAdvisor AI</h1>
            <p className="text-sm text-green-100">AI-powered crop advisory for every farmer</p>
          </div>
          <LanguageToggle language={language} onToggle={handleLanguageToggle} disabled={isLoading} />
        </div>
      </header>

      <main className="mx-auto w-full max-w-6xl px-4 py-5">
        <div className="mb-4 flex gap-2">
          <button
            type="button"
            onClick={() => setActiveTab("diagnose")}
            className={`rounded-md px-3 py-2 text-sm font-semibold ${
              activeTab === "diagnose" ? "bg-green-600 text-white" : "bg-gray-100 text-gray-700"
            }`}
          >
            Diagnose
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("chat")}
            disabled={!currentDiagnosis}
            className={`rounded-md px-3 py-2 text-sm font-semibold ${
              activeTab === "chat" ? "bg-green-600 text-white" : "bg-gray-100 text-gray-700"
            } disabled:cursor-not-allowed disabled:bg-gray-200`}
          >
            Chat
          </button>
        </div>

        {activeTab === "diagnose" && (
          <div className="grid gap-5 lg:grid-cols-2">
            <section className="rounded-xl bg-gray-100 p-5 shadow-sm">
              <h2 className="mb-3 text-lg font-semibold">Upload and Describe</h2>
              <UploadZone onFileChange={setSelectedFile} />
              <label className="mt-4 block text-sm font-medium text-gray-700">Describe the crop problem</label>
              <textarea
                value={description}
                onChange={(event) => setDescription(event.target.value)}
                className="mt-2 h-32 w-full rounded-lg border border-gray-300 p-3 text-sm focus:border-green-500 focus:outline-none"
                placeholder="Example: My maize leaves have long gray spots and plants are drying early."
              />
              <button
                type="button"
                onClick={handleDiagnose}
                disabled={!canDiagnose || isLoading}
                className="mt-4 w-full rounded-lg bg-green-600 px-4 py-2 font-semibold text-white hover:bg-green-700 disabled:cursor-not-allowed disabled:bg-gray-400"
              >
                {isLoading ? "Diagnosing..." : "Diagnose"}
              </button>
            </section>

            <section>
              {currentDiagnosis ? (
                <DiagnosisCard diagnosis={currentDiagnosis} onSuggestedQuestion={handleFollowup} />
              ) : (
                <div className="rounded-xl bg-gray-100 p-5 text-sm text-gray-600 shadow-sm">
                  Diagnosis results will appear here after you submit a photo and/or description.
                </div>
              )}
            </section>
          </div>
        )}

        {activeTab === "chat" && currentDiagnosis && (
          <section>
            <h2 className="mb-3 text-lg font-semibold">Follow-up Chat</h2>
            <ChatWindow history={conversationHistory} isLoading={isLoading} onSend={handleFollowup} />
          </section>
        )}
      </main>

      <footer className="border-t bg-gray-100">
        <div className="mx-auto w-full max-w-6xl px-4 py-4 text-center text-sm text-gray-600">
          Powered by Oxlo.ai | OxBuild Hackathon 2026
        </div>
      </footer>
    </div>
  );
}
