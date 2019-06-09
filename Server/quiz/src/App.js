import React from 'react';
import logo from './logo.svg';
import './App.css';
import Quiz from 'react-quiz-component';
import { quiz } from './quiz';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>
          Do you understand this word?
        </p>
        <Quiz quiz={quiz} showInstantFeedback={true} continueTillCorrect={true} onComplete={onCompleteAction}/>
      </header>
    </div>
  );
}

function onCompleteAction(e) {
  console.log(e)
}

export default App;
