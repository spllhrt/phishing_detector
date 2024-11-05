import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; 

export const detectPhishing = async (data) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/detect/`, data);
        return response; 
    } catch (error) {
        console.error('Error during phishing detection:', error);
        throw error; 
    }
};

export const registerUser = async (data) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/register/`, data);
        return response; 
    } catch (error) {
        console.error('Error during registration:', error);
        throw error; 
    }
};

export const loginUser = async (data) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/login/`, data);
        return response; 
    } catch (error) {
        console.error('Error during login:', error);
        throw error; 
    }
};
