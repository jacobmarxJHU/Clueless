import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import GamePage from './pages/GamePage';
import Login from './components/Login'; // Ensure this path is correct

function App() {

    return (
        <Router>
            <Routes>
                <Route path="/game/:gameCode" element={<GamePage />} />
                <Route path="/" element={<Login />} />
            </Routes>
        </Router>
    );
}

export default App;
