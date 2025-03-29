import React, { useState } from 'react';

const MCQuestion = ({ questionData, onNext }) => {
  const { question, options } = questionData;
  const [selectedOption, setSelectedOption] = useState(null);
  const [submitted, setSubmitted] = useState(false);

  const handleOptionClick = (index) => {
    if (!submitted) {
      setSelectedOption(index);
    }
  };

  const handleSubmitOrNext = () => {
    if (!submitted) {
      if (selectedOption === null) {
        alert("Please select an option before submitting.");
        return;
      }

      // If the selected answer is incorrect, store the question text in wrongQuestions.
      if (selectedOption !== correctIndex) {
        // Get the current wrongQuestions array from storage.
        chrome.storage.local.get('wrongQuestions', (result) => {
          let wrongArr = result.wrongQuestions || [];
          // Add the current question text.
          wrongArr.push(question);
          // Save the updated array back to storage.
          chrome.storage.local.set({ wrongQuestions: wrongArr }, () => {
            console.log("Stored wrong question:", question);
          });
        });
      }
      
      setSubmitted(true);
    } else {
      onNext();
    }
  };

  const correctIndex = options.findIndex(option => option.correct);
  const correctExplanation = options[correctIndex]?.explanation || '';

  return (
    <div style={{
      margin: '1rem 0',
      padding: '1rem',
      border: '1px solid #ccc',
      borderRadius: '4px'
    }}>
      <h3>{question}</h3>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {options.map((option, index) => {
          let style = {
            padding: '0.5rem',
            cursor: 'pointer',
            border: '1px solid #ccc',
            marginBottom: '0.5rem'
          };

          if (submitted) {
            if (option.correct) {
              style.backgroundColor = '#c8e6c9'; // light green for correct answer
            } else if (index === selectedOption) {
              style.backgroundColor = '#ffcdd2'; // light red for selected wrong answer
            }
          } else if (index === selectedOption) {
            style.backgroundColor = '#e0e0e0'; // highlight selected option before submit
          }
          return (
            <li key={index} style={style} onClick={() => handleOptionClick(index)}>
              {option.text}
            </li>
          );
        })}
      </ul>
      {submitted && (
        <div>
          <p><strong>Correct Answer:</strong> Option {correctIndex + 1}</p>
          <p><strong>Explanation:</strong> {correctExplanation}</p>
        </div>
      )}
      <button onClick={handleSubmitOrNext}>
        {submitted ? 'Next Question' : 'Submit'}
      </button>
    </div>
  );
};

export default MCQuestion;
