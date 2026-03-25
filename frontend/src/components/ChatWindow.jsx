import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";

export default function ChatWindow({ history, isLoading, onSend }) {
  const [message, setMessage] = useState("");
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [history, isLoading]);

  const submit = () => {
    const trimmed = message.trim();
    if (!trimmed || isLoading) return;
    onSend(trimmed);
    setMessage("");
  };

  return (
    <div className="rounded-xl bg-gray-100 p-4 shadow-sm">
      <div className="h-72 overflow-y-auto rounded-lg bg-white p-3">
        {history.map((msg, idx) => (
          <div
            key={`${msg.role}-${idx}`}
            className={`mb-3 flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[85%] rounded-lg px-3 py-2 text-sm ${
                msg.role === "user" ? "bg-green-600 text-white" : "bg-gray-200 text-gray-800"
              }`}
            >
              <ReactMarkdown>{msg.content}</ReactMarkdown>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="mb-3 flex justify-start">
            <div className="rounded-lg bg-gray-200 px-3 py-2 text-sm text-gray-700">Typing...</div>
          </div>
        )}

        <div ref={endRef} />
      </div>

      <div className="mt-3 flex gap-2">
        <input
          type="text"
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter") submit();
          }}
          placeholder="Ask a follow-up question"
          className="flex-1 rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-green-500 focus:outline-none"
        />
        <button
          type="button"
          onClick={submit}
          disabled={isLoading || !message.trim()}
          className="rounded-lg bg-green-600 px-4 py-2 text-sm font-semibold text-white hover:bg-green-700 disabled:cursor-not-allowed disabled:bg-gray-400"
        >
          Send
        </button>
      </div>
    </div>
  );
}
