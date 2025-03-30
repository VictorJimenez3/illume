
import React, { useState } from 'react';

const MCQuestion = ({ questionData, onNext }) => {
  const { question, options } = questionData;
  const [selectedOption, setSelectedOption] = useState(null);
  const [submitted, setSubmitted] = useState(false);

  // const correctIndex = options.findIndex(option => option.correct);
  const correctIndex = Math.floor(Math.random() * options[0].length);
  const correctExplanation = options[correctIndex]?.text || '';

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

      // Save incorrect questions to local storage
      if (selectedOption !== correctIndex) {
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
      animation: 'fadeSlide 0.3s ease'
    },
    questionText: {
      fontSize: '1.1rem',
      fontWeight: 'bold',
      marginBottom: '1rem'
    },
    option: {
      padding: '0.75rem',
      borderRadius: '8px',
      border: '1px solid #cfcfcf',
      marginBottom: '0.5rem',
      cursor: 'pointer',
      transition: 'all 0.2s ease'
    },
    selected: {
      backgroundColor: '#f6d3c5'
    },
    correct: {
      backgroundColor: '#c8e6c9'
    },
    incorrect: {
      backgroundColor: '#ffcdd2'
    },
    explanation: {
      marginTop: '1rem',
      backgroundColor: '#fceee3',
      border: '1px solid #e4b7a0',
      padding: '0.75rem',
      borderRadius: '8px'
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
      cursor: 'pointer'
    }
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

      <ul style={{ listStyle: 'none', padding: 0 }}>
        {options.map((option, index) => {
          let optionStyle = { ...styles.option };

          // if (submitted) {
          //   if (option.correct) {
          //     optionStyle = { ...optionStyle, ...styles.correct };
          //   } else if (index === selectedOption) {
          //     optionStyle = { ...optionStyle, ...styles.incorrect };
          //   }
          // } else if (index === selectedOption) {
          //   optionStyle = { ...optionStyle, ...styles.selected };
          // }

          if (submitted) {
            if (index == correctIndex) {
              optionStyle = { ...optionStyle, ...styles.correct };
            } else if (index === selectedOption) {
              optionStyle = { ...optionStyle, ...styles.incorrect };
            }
          } else if (index === selectedOption) {
            optionStyle = { ...optionStyle, ...styles.selected };
          }

          return (
            <li
              key={index}
              style={optionStyle}
              onClick={() => handleOptionClick(index)}
            >
              {option.text}
            </li>
          );
        })}
      </ul>

      {submitted && (
        <div style={styles.explanation}>
          <p><strong>Correct Answer:</strong> {options[correctIndex]?.text || "ALL FALSE"}</p>
          <p><strong>Explanation:</strong> {correctExplanation}</p>
        </div>
      )}

      <button onClick={handleSubmitOrNext} style={styles.button}>
        {submitted ? 'Next Question' : 'Submit'}
      </button>
    </div>
  );
};

export default MCQuestion;
