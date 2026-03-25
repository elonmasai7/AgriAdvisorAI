import React from 'react';

const SeverityBadge = ({ severity, score }) => {
    const getColor = () => {
        switch (severity.toLowerCase()) {
            case 'mild':
                return 'bg-green-100 text-green-800';
            case 'moderate':
                return 'bg-yellow-100 text-yellow-800';
            case 'severe':
                return 'bg-red-100 text-red-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    };

    return (
        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getColor()}`}>
            {severity} ({score}/10)
        </span>
    );
};

export default SeverityBadge;