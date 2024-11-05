import React, { useState } from 'react';
import { detectPhishing } from '../api/axiosConfig';
import 'bootstrap/dist/css/bootstrap.min.css'; 

function PhishingDetector() {
    const [sender, setSender] = useState('');
    const [subject, setSubject] = useState('');
    const [content, setContent] = useState('');
    const [result, setResult] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null); 

    const handleSubmit = async (event) => {
        event.preventDefault();

        const data = {
            sender: sender,
            subject: subject,
            content: content
        };

        try {
            setIsLoading(true); 
            setError(null);
            const response = await detectPhishing(data); 
            console.log('API Response:', response);
            setResult(response.data); 
        } catch (error) {
            console.error('Error detecting phishing:', error);
            setError('There was an error detecting phishing. Please try again.');
        } finally {
            setIsLoading(false); 
        }
    };

    return (
        <div className="container mt-5">
            <h2 className="text-center mb-4">Phishing Email Detector</h2>
            <p className="text-center mb-4">Enter the details of the email below to check for potential phishing attempts.</p>
            <div className="card shadow-lg">
                <div className="card-body">
                    <form onSubmit={handleSubmit}>
                        <div className="mb-3">
                            <label className="form-label">Sender:</label>
                            <input 
                                type="email" 
                                className="form-control" 
                                value={sender} 
                                onChange={(e) => setSender(e.target.value)} 
                                placeholder="e.g., sender@example.com" 
                                required 
                            />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Subject:</label>
                            <input 
                                type="text" 
                                className="form-control" 
                                value={subject} 
                                onChange={(e) => setSubject(e.target.value)} 
                                placeholder="Email Subject" 
                                required 
                            />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Content:</label>
                            <textarea 
                                className="form-control" 
                                value={content} 
                                onChange={(e) => setContent(e.target.value)} 
                                placeholder="Paste the email content here..." 
                                required 
                                rows="4"
                            />
                        </div>
                        <button type="submit" className="btn btn-primary btn-block">Check Email</button>
                    </form>
                    {isLoading && <p className="text-center mt-3">Loading...</p>} 
                    {error && <p className="text-danger text-center mt-3">{error}</p>} 
                    
                    <div className="mt-4">
                        <h5 className="text-center">Phishing Result:</h5>
                        <div className={`alert ${result?.is_phishing ? 'alert-danger' : result !== null ? 'alert-success' : ''}`} role="alert">
                            {result ? (result.is_phishing ? 'Phishing Detected!' : 'Not Phishing') : 'Result Pending...'}
                        </div>
                        <p className="text-center">{result ? result.message : "Initial message: Checking..."}</p>
                        <p className="text-center">Confidence Score: {result ? result.confidence_score : "0"} / 100</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default PhishingDetector;
