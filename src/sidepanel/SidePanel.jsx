import React, { useEffect, useState } from 'react';
import Quiz from '../quiz/Quiz';
import { fetchNewQuestions, fetchSummary, fetchSummaryAdjustments } from '../api_helpers';
import { getStorageValue } from '../utils'; 


const SidePanel = () => {
  const [selectedWord, setSelectedWord] = useState('');
//   const [summary, setSummary] = useState('');
  const [summaryArr, setSummaryArr] = useState([]);
  const [detailedSummary, setDetailedSummary] = useState([]);
  const [currentSummaryIndex, setCurrentSummaryIndex] = useState(0); // for carousel

//   const [detailedExplanation, setDetailedExplanation] = useState('');
  const [showDetailed, setShowDetailed] = useState(false);
  const [showQuiz, setShowQuiz] = useState(false);

  useEffect(() => {

    const fetchAndDisplaySummary = async () => {
      const word = await getStorageValue("selectedText");
      setSelectedWord(word);

      if (word) {
        try {
          const siteText = await getStorageValue("siteText");
          // Make the API call with POST body containing the keyword and full site text.
          const data = await fetchSummary(word, siteText);
          chrome.storage.local.set({ summary: data.general_explanation });
          setSummaryArr(prev => [data.general_explanation, ...prev]);
        //   setSummary(data.general_explanation);
          if (data.detailed_explanation) {
            // chrome.storage.local.set({ detailedExplanation: data.detailed_explanation });
            setDetailedSummary(data.detailed_explanation);
          }
        } catch (error) {
          console.error("Error fetching summary:", error);
        }
      } else {
        setSummaryArr(["No summary selected"]);
      }
    };

    fetchAndDisplaySummary();
  }, []);

  const openQuizModal = () => {
    setShowQuiz(true);
  };

  const closeQuizModal = () => {
     
    // console.log("Closing quiz modal");
    // // make API call to get new questions
    // try {
    //     // const siteText = await getStorageValue("siteText");
    //     const siteText = "dummy site text about nothing crazy";
    //     const wrong_questions = await getStorageValue("wrong_questions");

    //     // Make the API call to fetch new questions
    //     const data = await fetchNewQuestions(word, siteText, wrong_questions);


    //     // chrome.storage.local.set({ quiz_questions: data.questions });
    //     // chrome.storage.local.set({ new_questions_feedback: data.questions_raw });
    //     // chrome.storage.local.set({ new_answers_feedback: data.answers_raw });

    //     chrome.storage.local.set({ quiz_questions: data.questions }, function () {
    //         console.log("Quiz questions stored in local storage");
    //     });

    //     // try {
    //     //     // API call for summary adjustments
    //     //     const newData = await fetchSummaryAdjustments(word, data.new_questions, data.new_answers);
    //     //     setSummaryArr(prev => [newData.summary_adjustment, ...prev]);
            

    //     // } catch (error) {
    //     //     console.error("Error fetching summary adjustments:", error);
    //     // }

        

    // } catch (error) {
    //     console.error("Error fetching new questions:", error);
    // }



    setShowQuiz(false);
  };

  const toggleDetailed = () => {
    setShowDetailed(!showDetailed);
  };

  // Carousel controls
  const handleNextSummary = () => {
    setCurrentSummaryIndex((prev) => (prev + 1) % summaryArr.length);
  };

  const handlePrevSummary = () => {
    setCurrentSummaryIndex((prev) =>
      prev === 0 ? summaryArr.length - 1 : prev - 1
    );
  };

  const handleRefreshSummary = async () => {
    // Optionally, you might reset currentSummaryIndex to 0.

    try {
        // API call for summary adjustments
        const new_questions = "dummy new questions";
        const new_answers = "dummy new answers";
        const newData = await fetchSummaryAdjustments(word, new_questions, new_answers);
        setSummaryArr(prev => [newData.summary_adjustment, ...prev]);


    } catch (error) {
        console.error("Error fetching summary adjustments:", error);
    }


    // await fetchAndUpdateSummary();
  };

  return (
    <div style={{
      padding: '1.5rem',
      fontFamily: 'math',
      backgroundColor: '#f6eee0',
      color: '#a45c40',
      minHeight: '100vh'
    }}>
      <h2 style={{
        textAlign: 'center',
        color: '#3D0C0C',
        // backgroundColor: '#a45c40',
        padding: '0.75rem',
        borderRadius: '12px',
        fontSize: '1.5rem',
        marginBottom: '1rem',
      }}>
        illume
      </h2>
  
      <p style={{
        fontSize: '2rem',
        fontWeight: 'bold',
        color: '#a45c40',
        overflow: 'hidden',
        textOverflow: 'ellipsis',
        whiteSpace: 'nowrap',
        maxWidth: '100%',
        textAlign: 'center',
        fontStyle: 'italic',
      }}>
        {selectedWord?.length > 50
          ? selectedWord.slice(0, 50) + '...'
          : selectedWord || "No word selected."}
      </p>
  
      {summaryArr.length === 0 && (
        <div>
          <p>Loading summary...</p>
          <progress style={{ width: '100%', color: '#a45c40' }} />
        </div>
      )}
  
      {summaryArr.length > 0 && (
        <div style={{
          backgroundColor: '#e4b7a0',
          color: '#3a2c1b',
          border: '1px solid #c38370',
          padding: '1rem',
          marginTop: '1rem',
          borderRadius: '10px'
        }}>
         <p style={{ textAlign: 'center', fontWeight: 'bold', marginBottom: '0.5rem' }}>
            Summary {currentSummaryIndex + 1} of {summaryArr.length}
            </p>
          {summaryArr.length > 0 && (
            <div style={{
                marginTop: '1rem',
              backgroundColor: '#fff5ea',
              border: '1px solid #c38370',
              borderRadius: '8px',
              padding: '0.75rem',
              textAlign: 'center',
              maxHeight: '200px',
              overflowY: 'auto',
            }}>
                <p style={{
                fontSize: '1.1rem',
                // fontWeight: 'bold',
                // lineHeight: '1.2',
                // whiteSpace: 'pre-line'
                }}>
                {summaryArr[currentSummaryIndex]}
                </p>
            </div>
         )}
  
          
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              marginTop: '1rem'
            }}>
              <button
                onClick={handlePrevSummary}
                style={{
                  backgroundColor: '#c38370',
                  borderColor: '#c38370',
                //   border: 'none',
                //   padding: '0.5rem 1rem',
                  borderRadius: '6px',
                  color: 'white',
                  cursor: 'pointer'
                }}
              >
                ◀
              </button>
              <button
                onClick={handleNextSummary}
                style={{
                  backgroundColor: '#c38370',
                  borderColor: '#c38370',
                //   padding: '0.5rem 1rem',
                  borderRadius: '6px',
                  color: 'white',
                  cursor: 'pointer'
                }}
              >
                ▶
              </button>
            </div>

            <button onClick={handleRefreshSummary} style={{
                position: 'absolute',
                bottom: '10px',
                right: '10px',
                backgroundColor: '#e4b7a0',
                border: 'none',
                padding: '0.4rem 0.8rem',
                borderRadius: '6px',
                color: '#a45c40',
                cursor: 'pointer'
            }}>
                🔄
            </button>
          
  
          <div style={{ marginTop: '1rem', textAlign: 'center' }}>
            <button
              onClick={toggleDetailed}
              style={{
                backgroundColor: '#a45c40',
                color: 'white',
                padding: '0.5rem 1rem',
                border: 'none',
                borderRadius: '6px',
                cursor: 'pointer',
                
              }}
            >
              {showDetailed ? "Hide Contextualized Explanation" : "Contextualize Now!"}
            </button>
          </div>
  
          {showDetailed && (
            <div style={{
              marginTop: '1rem',
              backgroundColor: '#fff5ea',
              border: '1px solid #c38370',
              borderRadius: '8px',
              padding: '0.75rem',
              textAlign: 'center',
              maxHeight: '200px',
              overflowY: 'auto',
            }}>
              <p>{detailedSummary || "No contextualized explanation available."}</p>
            </div>
          )}
        </div>
        
      )}
  
      <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
        <button
          id="learnMoreButton"
          onClick={openQuizModal}
          style={{
            backgroundColor: '#a45c40',
            color: 'white',
            padding: '0.75rem 1.5rem',
            border: 'none',
            borderRadius: '8px',
            fontWeight: 'bold',
            fontSize: '1rem',
            cursor: 'pointer',
          }}
        >
          Open Quiz
        </button>
      </div>
  
      {showQuiz && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          background: 'rgba(0, 0, 0, 0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000
        }}>
          <div style={{
            background: 'white',
            padding: '1.5rem',
            borderRadius: '12px',
            width: '90%',
            maxWidth: '600px',
            boxShadow: '0 0 20px rgba(0,0,0,0.2)'
          }}>
            <Quiz
              selectedWord={selectedWord}
              summary={summaryArr[currentSummaryIndex]}
              onExit={closeQuizModal}
            />
          </div>
        </div>
      )}
    </div>
  );
  
};

export default SidePanel;
