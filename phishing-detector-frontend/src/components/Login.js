import React, { useState } from 'react';
import { loginUser } from '../api/axiosConfig'; 

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const handleSubmit = async (event) => {
        event.preventDefault();
    
        const data = {
            email: email,
            password: password,
        };
    
        try {
            const response = await loginUser(data);
            console.log('Login Response:', response.data);
            setSuccess('Login successful!'); 
            setError(null); 
        } catch (error) {
            console.error('Login failed:', error);
            setError('Invalid credentials'); 
            setSuccess(null); 
        }
    };

    return (
        <div className="container mt-5">
            <h2 className="text-center mb-4">Login to Your Account</h2>
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <div className="card p-4 shadow">
                        <form onSubmit={handleSubmit}>
                            <div className="mb-3">
                                <label className="form-label">Email:</label>
                                <input
                                    type="email"
                                    className="form-control"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="mb-3">
                                <label className="form-label">Password:</label>
                                <input
                                    type="password"
                                    className="form-control"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                />
                            </div>
                            <button type="submit" className="btn btn-primary btn-block">Login</button>
                        </form>
                        {error && <p className="text-danger mt-3">{error}</p>}
                        {success && <p className="text-success mt-3">{success}</p>}
                    </div>
                    <p className="text-center mt-3">
                        Don't have an account? <a href="/register">Register here</a>
                    </p>
                </div>
            </div>
        </div>
    );
}

export default Login;
