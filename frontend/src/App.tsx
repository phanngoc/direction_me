import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// Import components (will be created in later tasks)
// import ChatbotInterface from './chatbot/ChatbotInterface';
// import AssessmentPage from './assessment/AssessmentPage';
// import ResultsPage from './visualization/ResultsPage';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>MyWay - Chatbot Assessment Interface</h1>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<div>Welcome to MyWay Assessment Platform</div>} />
            {/* Routes will be added in later tasks */}
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
