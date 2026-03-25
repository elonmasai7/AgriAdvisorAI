import axios from 'axios';

const API_BASE = 'http://localhost:8000';

export async function diagnose(imageFile, description, language) {
    const formData = new FormData();
    if (imageFile) {
        formData.append('file', imageFile);
    }
    formData.append('description', description);
    formData.append('language', language);

    const response = await axios.post(`${API_BASE}/diagnose`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
}

export async function followUp(message, history, language) {
    const response = await axios.post(`${API_BASE}/followup`, {
        message,
        conversation_history: history,
        language,
    });
    return response.data.reply;
}