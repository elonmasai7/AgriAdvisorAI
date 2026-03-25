import { useState } from "react";
import ReactMarkdown from "react-markdown";

import SeverityBadge from "./SeverityBadge";

export default function DiagnosisCard({ diagnosis, onSuggestedQuestion }) {
  const [treatmentTab, setTreatmentTab] = useState("organic");

  if (!diagnosis) return null;

  const treatmentTabs = ["organic", "chemical", "cultural"];
  const progress = Math.min(Math.max(Number(diagnosis.severity_score || 0), 1), 10) * 10;

  return (
    <div className="rounded-xl bg-gray-100 p-5 shadow-sm">
      <h2 className="text-2xl font-bold text-gray-900">
        {diagnosis.crop_detected} | {diagnosis.disease_identified}
      </h2>

      <div className="mt-3 flex flex-wrap items-center gap-3">
        <SeverityBadge severity={diagnosis.severity} score={diagnosis.severity_score} />
        <span className="rounded-full bg-white px-3 py-1 text-sm font-medium text-gray-700">
          Confidence: {diagnosis.confidence}
        </span>
      </div>

      <div className="mt-4">
        <p className="mb-1 text-sm font-semibold text-gray-700">Severity score</p>
        <div className="h-3 w-full rounded-full bg-white">
          <div
            className="h-3 rounded-full bg-green-600 transition-all"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      <section className="mt-5">
        <h3 className="text-lg font-semibold text-gray-900">Diagnosis Summary</h3>
        <div className="prose prose-sm mt-2 max-w-none text-gray-700">
          <ReactMarkdown>{diagnosis.diagnosis_summary}</ReactMarkdown>
        </div>
      </section>

      <section className="mt-5">
        <h3 className="text-lg font-semibold text-gray-900">Treatment Plan</h3>
        <div className="mt-2 flex gap-2">
          {treatmentTabs.map((tab) => (
            <button
              key={tab}
              type="button"
              onClick={() => setTreatmentTab(tab)}
              className={`rounded-md px-3 py-1 text-sm font-semibold capitalize ${
                treatmentTab === tab
                  ? "bg-green-600 text-white"
                  : "bg-white text-gray-700 hover:bg-gray-200"
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
        <div className="prose prose-sm mt-3 max-w-none rounded-lg bg-white p-3 text-gray-700">
          <ReactMarkdown>{diagnosis.treatment_plan?.[treatmentTab] || "Not available."}</ReactMarkdown>
        </div>
      </section>

      <section className="mt-5">
        <h3 className="text-lg font-semibold text-gray-900">Prevention Advice</h3>
        <div className="prose prose-sm mt-2 max-w-none text-gray-700">
          <ReactMarkdown>{diagnosis.prevention_advice}</ReactMarkdown>
        </div>
      </section>

      {diagnosis.severity_score > 5 && (
        <section className="mt-5 rounded-lg border border-orange-300 bg-orange-50 p-3">
          <h3 className="font-semibold text-orange-800">Yield Loss Warning</h3>
          <div className="prose prose-sm mt-1 max-w-none text-orange-900">
            <ReactMarkdown>{diagnosis.yield_loss_warning}</ReactMarkdown>
          </div>
        </section>
      )}

      <section className="mt-5">
        <h3 className="text-lg font-semibold text-gray-900">Suggested Follow-up Questions</h3>
        <div className="mt-2 flex flex-wrap gap-2">
          {(diagnosis.follow_up_questions || []).map((question) => (
            <button
              key={question}
              type="button"
              onClick={() => onSuggestedQuestion(question)}
              className="rounded-full bg-white px-3 py-1 text-sm text-green-700 hover:bg-green-100"
            >
              {question}
            </button>
          ))}
        </div>
      </section>

      <section className="mt-5 text-sm text-gray-600">
        <span className="font-semibold">Sources:</span> {(diagnosis.sources_consulted || []).join(", ")}
      </section>
    </div>
  );
}
