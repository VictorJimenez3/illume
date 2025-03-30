import React, { useState } from 'react';

const OEQuestion = ({ questionData, onNext }) => {
  const { question, options } = questionData;
  // For open ended questions, assume there's one option with the correct answer.
  const correctAnswer = options[0].text;
  const explanation = options[0].explanation;

  const [userAnswer, setUserAnswer] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);

  const handleSubmitOrNext = () => {
    if (!submitted) {
      const normalizedUserAnswer = userAnswer.trim().toLowerCase();
      const normalizedCorrectAnswer = correctAnswer.trim().toLowerCase();
      const check = normalizedUserAnswer && normalizedCorrectAnswer.includes(normalizedUserAnswer);
      setIsCorrect(check);

        // If the answer is incorrect, store the question text in wrongQuestions.
      if (!check) {
        // Get the current wrongQuestions array from storage.
        chrome.storage.local.get('wrong_questions', (result) => {
            let wrongArr = result.wrong_questions || [];
            // Add the current question text.
            wrongArr.push(question);
            // Save the updated array back to storage.
            chrome.storage.local.set({ wrong_questions: wrongArr }, () => {
            console.log("Stored wrong question:", question);
            });
       });
      }


      setSubmitted(true);
    } else {
      onNext();
    }
  };

  return (
    <div style={{
      margin: '1rem 0',
      padding: '1rem',
      border: '1px solid #ccc',
      borderRadius: '4px'
    }}>
      <h3>{question}</h3>
      {!submitted ? (
        <input
          type="text"
          value={userAnswer}
          onChange={(e) => setUserAnswer(e.target.value)}
          placeholder="Type your answer here"
          style={{ width: '100%', padding: '0.5rem', marginBottom: '1rem' }}
        />
      ) : (
        <div>
          <p><strong>Your Answer:</strong> {userAnswer}</p>
          {isCorrect ? (
            <p style={{ color: 'green' }}>Correct!</p>
          ) : (
            <p style={{ color: 'red' }}>Incorrect.</p>
          )}
          <p><strong>Correct Answer:</strong> {correctAnswer}</p>
          <p><strong>Explanation:</strong> {explanation}</p>
        </div>
      )}
      <button onClick={handleSubmitOrNext}>
        {submitted ? 'Next Question' : 'Submit'}
      </button>
    </div>
  );
};

export default OEQuestion;
