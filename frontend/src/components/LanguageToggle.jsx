import React from 'react';

const LanguageToggle = ({ language, onToggle }) => {
    return (
        <button
            onClick={onToggle}
            className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
            {language === 'en' ? 'EN' : 'SW'}
        </button>
    );
};

export default LanguageToggle;