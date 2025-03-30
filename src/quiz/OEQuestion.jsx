import React, { useState } from 'react';

const OEQuestion = ({ questionData, onNext }) => {
  const { question, options } = questionData;
  const correctAnswer = options[0].text;
  const explanation = options[0].explanation;

  const [userAnswer, setUserAnswer] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);

  const handleSubmitOrNext = () => {
    if (!submitted) {
      const normalizedUserAnswer = userAnswer.trim().toLowerCase();
      const normalizedCorrectAnswer = correctAnswer.trim().toLowerCase();
      const check = normalizedCorrectAnswer.includes(normalizedUserAnswer);
      setIsCorrect(check);

      if (!check) {
        chrome.storage.local.get('wrong_questions', (result) => {
          let wrongArr = result.wrong_questions || [];
          wrongArr.push(question);
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

  const styles = {
    container: {
      backgroundColor: '#fffaf3',
      border: '1px solid #c38370',
      borderRadius: '12px',
      padding: '1rem',
      margin: '1rem 0',
      color: '#a45c40',
      animation: 'fadeSlide 0.3s ease',
    },
    questionText: {
      fontSize: '1.1rem',
      fontWeight: 'bold',
      marginBottom: '1rem',
    },
    input: {
      width: '90%',
      padding: '0.75rem',
      borderRadius: '8px',
      border: '1px solid #ccc',
      marginBottom: '1rem',
      fontSize: '1rem',
    },
    feedback: {
      marginTop: '0.5rem',
    },
    correctText: {
      color: 'green',
      fontWeight: 'bold',
    },
    incorrectText: {
      color: 'red',
      fontWeight: 'bold',
    },
    explanation: {
      marginTop: '1rem',
      backgroundColor: '#fceee3',
      border: '1px solid #e4b7a0',
      padding: '0.75rem',
      borderRadius: '8px',
    },
    button: {
      marginTop: '1rem',
      backgroundColor: '#a45c40',
      color: 'white',
      padding: '0.6rem 1.25rem',
      border: 'none',
      borderRadius: '8px',
      fontWeight: 'bold',
      fontSize: '1rem',
      cursor: 'pointer',
    },
  };

  return (
    <div style={styles.container}>
      <style>
        {`
          @keyframes fadeSlide {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
          }
        `}
      </style>

      <div style={styles.questionText}>{question}</div>

      {!submitted ? (
        <input
          type="text"
          value={userAnswer}
          onChange={(e) => setUserAnswer(e.target.value)}
          placeholder="Type your answer here"
          style={styles.input}
        />
      ) : (
        <div style={styles.feedback}>
          <p><strong>Your Answer:</strong> {userAnswer}</p>
          {isCorrect ? (
            <p style={styles.correctText}>Correct!</p>
          ) : (
            <p style={styles.incorrectText}>Incorrect.</p>
          )}
          <div style={styles.explanation}>
            <p><strong>Correct Answer:</strong> {correctAnswer}</p>
            <p><strong>Explanation:</strong> {explanation}</p>
          </div>
        </div>
      )}

      <button onClick={handleSubmitOrNext} style={styles.button}>
        {submitted ? 'Next Question' : 'Submit'}
      </button>
    </div>
  );
};

export default OEQuestion;
