import React, { useState, useEffect } from 'react';
import MCQuestion from './MCQuestion';
import OEQuestion from './OEQuestion';
import { fetchQuestions } from '../api_helpers';
import { getStorageValue } from '../utils'; 


const Quiz = ({ selectedWord, summary, onExit }) => {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

//   const defaultQuestions = [
//     {
//       question: "Fetching Quiz Questions...",
//       type: "mc",
//       options: [
//         // { text: "Paris", correct: true, explanation: "Paris is the capital of France." },
//         // { text: "London", correct: false, explanation: "London is the capital of the United Kingdom." },
//         // { text: "Berlin", correct: false, explanation: "Berlin is the capital of Germany." },
//         // { text: "Rome", correct: false, explanation: "Rome is the capital of Italy." }
//       ]
//     }];

  useEffect(() => {
    const fetchAndDisplayQuestions = async () => {
      
    //   setQuestions(defaultQuestions);
      // check if quiz_questions is already in local storage
      const quizQuestions = await getStorageValue('quiz_questions');
      if (quizQuestions) {
            setQuestions(quizQuestions);
            // clear quiz_questions from local storage
            chrome.storage.local.remove('quiz_questions', () => {
                console.log("Cleared quiz questions from local storage");
            });
      } else {
        try {
            const data = await fetchQuestions(selectedWord, summary);
            setQuestions(data.questions);
          } catch (error) {
            console.error("Error fetching questions:", error);
            setQuestions([]);
          }
      }
    };

    fetchAndDisplayQuestions();

    // Clear wrong_questions from local storage when the component mounts
    chrome.storage.local.remove('wrong_questions', () => {
      console.log("Cleared wrong questions from local storage");
    });

    // For now, use default questions
    // setQuestions(defaultQuestions);
  }, []);

//   const handleWrongAnswer = (questionText) => {
//     setWrongQuestions(prev => [...prev, questionText]);
//   };

  const handleNextQuestion = () => {
    // const isLastQuestion = currentIndex + 1 === questions.length;
    // if (isLastQuestion) {


        
    //   chrome.storage.local.set({ wrong_questions: wrongQuestions }, () => {
    //     // console.log("Wrong questions saved to local storage:", wrongAnswers);
    //   });
    // }
    setCurrentIndex(prev => prev + 1);
  };

  const totalQuestions = questions.length;
  const currentQuestionNumber = currentIndex + 1;
  const currentQuestion = questions[currentIndex];

  return (
    <div style={{ fontFamily: 'sans-serif' }}>
      <h2>Quiz</h2>
      {totalQuestions === 0 && (
        <div>
          <p>Loading questions...</p>
          <progress style={{ width: '100%' }} />
        </div>
      )}
      {totalQuestions > 0 && currentIndex < totalQuestions ? (
        <>
          <div style={{ marginBottom: '1rem' }}>
            <progress value={currentQuestionNumber} max={totalQuestions} style={{ width: '100%' }} />
            <p>Question {currentQuestionNumber} of {totalQuestions}</p>
          </div>
          {currentQuestion.type === 'mc' ? (
            <MCQuestion
              key={currentIndex}
              questionData={currentQuestion}
              onNext={handleNextQuestion}
            //   onWrong={handleWrongAnswer}
            />
          ) : (
            <OEQuestion
              key={currentIndex}
              questionData={currentQuestion}
              onNext={handleNextQuestion}
            //   onWrong={handleWrongAnswer}
            />
          )}
        </>
      ) : (
        <div>
          {totalQuestions > 0 ? <p>You have completed the quiz!</p> : <p></p>}
          <button onClick={onExit}>Exit Quiz</button>
        </div>
      )}
    </div>
  );
};

export default Quiz;
