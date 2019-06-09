import React from 'react';
import logo from './logo.svg';
import './App.css';
import Quiz from 'react-quiz-component';
import { quiz } from './quiz';
import { Entity } from './Entity';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>
          Do you understand this word?
        </p>
        <Quiz quiz={quiz} showInstantFeedback={true} onComplete={onCompleteAction}/>
      </header>
    </div>
  );
}

function onCompleteAction(e) {
  let correct = [];
  let incorrect = [];
  for(let i = 0; i < this.correct.length; i++){
    correct.push(e.questions[this.correct[i]].question);
    console.log(e.questions[this.correct[i]].question);
  }
  for(let j = 0; j < this.incorrect.length; j++){
    incorrect.push(e.questions[this.incorrect[j]].question);
    console.log(e.questions[this.incorrect[j]].question);
  }
  console.log(correct);
  console.log(incorrect);
  let correctstring = "";
  for(let k = 0; k < correct.length; k++){
    correctstring += correct[k] + ",";
  }
  let incorrectstring = "";
  for(let k = 0; k < incorrect.length; k++){
    incorrectstring += incorrect[k] + ",";
  }
  Entity.sendCorrectIncorrect(correctstring, incorrectstring);

}

export default App;

