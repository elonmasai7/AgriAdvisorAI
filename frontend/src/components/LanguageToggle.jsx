export default function LanguageToggle({ language, onToggle, disabled = false }) {
  return (
    <div className="inline-flex rounded-lg border border-green-300 bg-white p-1">
      <button
        type="button"
        onClick={() => onToggle("en")}
        disabled={disabled}
        className={`rounded-md px-3 py-1 text-sm font-semibold ${
          language === "en" ? "bg-green-600 text-white" : "text-green-700"
        }`}
      >
        EN
      </button>
      <button
        type="button"
        onClick={() => onToggle("sw")}
        disabled={disabled}
        className={`rounded-md px-3 py-1 text-sm font-semibold ${
          language === "sw" ? "bg-green-600 text-white" : "text-green-700"
        }`}
      >
        SW
      </button>
    </div>
  );
}
