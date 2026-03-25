import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import SeverityBadge from './SeverityBadge';

const DiagnosisCard = ({ diagnosis, onFollowUpClick }) => {
    const [activeTab, setActiveTab] = useState('organic');

    if (!diagnosis) return null;

    const treatmentTabs = ['organic', 'chemical', 'cultural'];

    return (
        <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold text-green-700 mb-4">
                {diagnosis.crop_detected} - {diagnosis.disease_identified}
            </h2>

            <div className="flex items-center gap-4 mb-4">
                <SeverityBadge severity={diagnosis.severity} score={diagnosis.severity_score} />
                <span className="text-sm text-gray-600">Confidence: {diagnosis.confidence}</span>
            </div>

            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Severity Score</label>
                <div className="w-full bg-gray-200 rounded-full h-4">
                    <div
                        className="bg-green-500 h-4 rounded-full"
                        style={{ width: `${(diagnosis.severity_score / 10) * 100}%` }}
                    ></div>
                </div>
                <span className="text-sm text-gray-600">{diagnosis.severity_score}/10</span>
            </div>

            <div className="mb-6">
                <h3 className="text-lg font-semibold mb-2">Diagnosis Summary</h3>
                <ReactMarkdown className="text-gray-700">{diagnosis.diagnosis_summary}</ReactMarkdown>
            </div>

            <div className="mb-6">
                <h3 className="text-lg font-semibold mb-2">Treatment Plan</h3>
                <div className="flex border-b">
                    {treatmentTabs.map((tab) => (
                        <button
                            key={tab}
                            onClick={() => setActiveTab(tab)}
                            className={`px-4 py-2 capitalize ${activeTab === tab ? 'border-b-2 border-green-500 text-green-600' : 'text-gray-600'
                                }`}
                        >
                            {tab}
                        </button>
                    ))}
                </div>
                <div className="mt-4 p-4 bg-gray-50 rounded">
                    <ReactMarkdown>{diagnosis.treatment_plan[activeTab]}</ReactMarkdown>
                </div>
            </div>

            <div className="mb-6">
                <h3 className="text-lg font-semibold mb-2">Prevention Advice</h3>
                <ReactMarkdown className="text-gray-700">{diagnosis.prevention_advice}</ReactMarkdown>
            </div>

            {diagnosis.severity_score > 5 && (
                <div className="mb-6 p-4 bg-orange-100 border-l-4 border-orange-500">
                    <h3 className="font-semibold text-orange-800">Yield Loss Warning</h3>
                    <ReactMarkdown className="text-orange-700">{diagnosis.yield_loss_warning}</ReactMarkdown>
                </div>
            )}

            <div className="mb-6">
                <h3 className="text-lg font-semibold mb-2">Suggested Follow-up Questions</h3>
                <div className="flex flex-wrap gap-2">
                    {diagnosis.follow_up_questions.map((question, index) => (
                        <button
                            key={index}
                            onClick={() => onFollowUpClick(question)}
                            className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm hover:bg-green-200"
                        >
                            {question}
                        </button>
                    ))}
                </div>
            </div>

            <div className="text-sm text-gray-500">
                <strong>Sources Consulted:</strong> {diagnosis.sources_consulted.join(', ')}
            </div>
        </div>
    );
};

export default DiagnosisCard;