import React, { useState, useEffect } from 'react';
import MCQuestion from './MCQuestion';
import OEQuestion from './OEQuestion';
import { fetchQuestions } from '../api_helpers'; // Adjust the import path as needed
import { getSelectedWord, getSummary } from '../sidepanel/SidePanel'; // Adjust the import path as needed

// Import OEQuestion if needed for open-ended questions

const Quiz = ({ onExit }) => {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  // For demo purposes, using default questions.
  // Replace this with your API call fetchQuestions() as needed.
  // Replace this default with your API call (fetchQuestions) as needed.
  const defaultQuestions = [
    {
      question: "What is the capital of France?",
      type: "mc",
      options: [
        { text: "Paris", correct: true, explanation: "Paris is the capital of France." },
        { text: "London", correct: false, explanation: "London is the capital of the United Kingdom." },
        { text: "Berlin", correct: false, explanation: "Berlin is the capital of Germany." },
        { text: "Rome", correct: false, explanation: "Rome is the capital of Italy." }
      ]
    },
    {
      question: "Which planet is known as the Red Planet?",
      type: "mc",
      options: [
        { text: "Mars", correct: true, explanation: "Mars is known as the Red Planet." },
        { text: "Venus", correct: false, explanation: "Venus is not the Red Planet." },
        { text: "Jupiter", correct: false, explanation: "Jupiter is the largest planet in our Solar System." }
      ]
    },
    // Open Ended Question as the last element
    {
      question: "Describe the process of photosynthesis.",
      type: "oe",
      options: [
        {
          text: "Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods from carbon dioxide and water. It involves the green pigment chlorophyll and produces oxygen as a byproduct.",
          explanation: "This process converts light energy into chemical energy stored in sugars."
        }
      ]
    }
  ];

  useEffect(() => {
    // Simulate API call; replace with fetchQuestions() as needed.
    const fetchAndDisplayQuestions = async () => {
        try {
            const data = await fetchQuestions(getSelectedWord(), getSummary());

            
            // Assume the API returns an object with a "questions" property (an array)
            setQuestions(data.questions);
        } catch (error) {
            console.error("Error fetching questions:", error);
            setQuestions(defaultQuestions); // Fallback to default questions
        }
    }

    fetchAndDisplayQuestions();
    
  }, []);

  const handleNextQuestion = () => {
    setCurrentIndex(prev => prev + 1);
  };

  const totalQuestions = questions.length;
  const currentQuestionNumber = currentIndex + 1;
  const currentQuestion = questions[currentIndex];

  return (
    <div style={{ fontFamily: 'sans-serif' }}>
      <h2>Quiz</h2>
      {totalQuestions > 0 && currentIndex < totalQuestions ? (
        <>
          {/* Progress Bar */}
          <div style={{ marginBottom: '1rem' }}>
            <progress value={currentQuestionNumber} max={totalQuestions} style={{ width: '100%' }} />
            <p>Question {currentQuestionNumber} of {totalQuestions}</p>
          </div>
          {currentQuestion.type === 'mc' ? (
                <MCQuestion
                key={currentIndex}
                questionData={currentQuestion}
                onNext={handleNextQuestion}
                />
            ) : (
                <OEQuestion
                key={currentIndex}
                questionData={currentQuestion}
                onNext={handleNextQuestion}
                />
            )}
        </>
      ) : (
        <div>
          <p>You have completed the quiz!</p>
          <button onClick={onExit}>Exit Quiz</button>
        </div>
      )}
    </div>
  );
};

export default Quiz;
