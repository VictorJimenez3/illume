import React, { useState, useEffect } from 'react';
import MCQuestion from './MCQuestion';
import OEQuestion from './OEQuestion';
import { fetchQuestions } from '../api_helpers';
import { getStorageValue } from '../utils';

const Quiz = ({ selectedWord, summary, onExit, onESC, isRefreshing }) => {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {

    // run onExit when escape pressed
    const handleKeyDown = (event) => {
      if (event.key === 'Escape') {
        onESC();
      }
    };
    document.addEventListener('keydown', handleKeyDown);


    const fetchAndDisplayQuestions = async () => {
      
        // Check if questions are already in local storage
        const storedQuestions = await getStorageValue('quiz_questions');
        if (storedQuestions) {
          setQuestions(storedQuestions);
          return;
        }


      try {
        const data = await fetchQuestions(selectedWord, summary);
        setQuestions(data.questions);

        // const questions_map = data.map(entry => entry.questions);
        // let questions_map = [];

        // iterate through data
        // add questions to questions_map
        // for (let i = 0; i < data.length; i++) {
        //     const question = data[i].questions;
        //     if (question) {
        //         questions_map.push(question);
        //     }
        // }


        // iterate through data and add ["questions"] to questions
        // setQuestions(questions_map);
        // chrome.storage.local.set({ quiz_questions: data.questions }, () => {
        //     console.log(questions);
        //     console.log(data);
        // });
      } catch (error) {
        console.error("Hang in there!", error);
        
        // try once more
        try {
            const data = await fetchQuestions(selectedWord, summary);
                setQuestions(data.questions);
                chrome.storage.local.set({ quiz_questions: data.questions }, () => {
                    console.log(JSON.stringify(data.questions, null, 4));
            });
        } catch (error) {
            console.error("Error fetching questions.", error);
            setQuestions([]);
            return;
        }
      }

      return () => {
        document.removeEventListener('keydown', handleKeyDown);
      }
    };

    fetchAndDisplayQuestions();

    chrome.storage.local.remove('wrong_questions', () => {
      console.log("Cleared wrong questions from local storage");
    });
  }, []);

  const handleNextQuestion = () => {
    setCurrentIndex(prev => prev + 1);
  };

  const totalQuestions = questions.length;
  const currentQuestionNumber = currentIndex + 1;
  const currentQuestion = questions[currentIndex];

  const styles = {
    container: {
      fontFamily: 'sans-serif',
      backgroundColor: '#f6eee0',
      color: '#a45c40',
      padding: '1.5rem',
      borderRadius: '12px',
      animation: 'fadeSlide 0.3s ease',
    },
    title: {
      textAlign: 'center',
      fontSize: '1.6rem',
      fontWeight: 'bold',
      color: '#a45c40',
      marginBottom: '1rem'
    },
    progressWrapper: {
      marginBottom: '1rem'
    },
    progressText: {
      marginTop: '0.5rem',
      textAlign: 'center',
      color: '#a45c40'
    },
    loading: {
      textAlign: 'center'
    },
    button: {
      marginTop: '1rem',
      backgroundColor: '#a45c40',
      color: 'white',
      padding: '0.75rem 1.5rem',
      border: 'none',
      borderRadius: '8px',
      fontWeight: 'bold',
      fontSize: '1rem',
      cursor: 'pointer'
    }
  };

  return (
    <div style={styles.container}>
      {/* Animation Keyframes (inline CSS trick) */}
      <style>
        {`
          @keyframes fadeSlide {
            from {
              opacity: 0;
              transform: translateY(10px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }
        `}
      </style>

      <h2 style={styles.title}>Quiz</h2>

      {totalQuestions === 0 && (
        <div style={styles.loading}>
          <p>Loading questions...</p>
          <progress style={{ width: '100%' , color: '#a45c40'}} />
        </div>
      )}

      {totalQuestions > 0 && currentIndex < totalQuestions ? (
        <>
          <div style={styles.progressWrapper}>
            <progress value={currentQuestionNumber} max={totalQuestions} style={{ width: '100%' }} />
            <p style={styles.progressText}>
              Question {currentQuestionNumber} of {totalQuestions}
            </p>
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
        <div style={styles.loading}>
          {totalQuestions > 0 && <p>You have completed the quiz!</p>}
          <button onClick={onExit} style={styles.button}>Exit Quiz</button>
          {isRefreshing && (
            <div style={styles.loading}>
            <p>Personalizing experience...</p>
            <progress style={{ width: '100%' , color: '#a45c40'}} />
            </div>
        )}
        </div>
      )}
    </div>
  );
};

export default Quiz;


