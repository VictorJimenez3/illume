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
    //     const siteText = await getStorageValue("siteText");
    //     const wrong_questions = await getStorageValue("wrong_questions");

    //     // Make the API call to fetch new questions
    //     const data = await fetchNewQuestions(word, siteText, wrong_questions);
    //     chrome.storage.local.set({ quiz_questions: data.questions });
    //     chrome.storage.local.set({ new_questions_feedback: data.questions_raw });
    //     chrome.storage.local.set({ new_answers_feedback: data.answers_raw });

    //     try {
    //         // API call for summary adjustments
    //         const newData = await fetchSummaryAdjustments(word, data.new_questions, data.new_answers);
    //         setSummaryArr(prev => [newData.summary_adjustment, ...prev]);
            

    //     } catch (error) {
    //         console.error("Error fetching summary adjustments:", error);
    //     }

        

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

  return (
    <div style={{ padding: '1rem', fontFamily: 'sans-serif', position: 'relative' }}>
      <h2>illume</h2>
      <p>{selectedWord || "No word selected."}</p>

      {summaryArr.length === 0 && (
        <div>
          <p>Loading summary...</p>
          <progress style={{ width: '100%' }} />
        </div>
      )}

      {summaryArr.length > 0 && (
        <div style={{ border: '1px solid #ccc', padding: '1rem', marginTop: '1rem', borderRadius: '6px' }}>
          <p><strong>Summary {currentSummaryIndex + 1} of {summaryArr.length}</strong></p>
          <p>{summaryArr[currentSummaryIndex]}</p>

          

          {/* diplay carousel buttons only if there are multiple summaries */}
          {summaryArr.length > 1 && (
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '1rem' }}>
            <button onClick={handlePrevSummary}>◀ Previous</button>
            <button onClick={handleNextSummary}>Next ▶</button>
            </div>
          )}


          <div style={{ marginTop: '1rem' }}>
            <button onClick={toggleDetailed}>
            {showDetailed ? "Hide Contextualized Explanation" : "Contextualize Now!"}
            </button>
          </div>

          {showDetailed && (
            <div style={{ marginTop: '1rem' }}>
            <p>{detailedSummary || "No contextualized explanation available."}</p>
            </div>
          )}
        </div>
      )}


      <div style={{ marginTop: '1rem' }}>
        <button id="learnMoreButton" onClick={openQuizModal}>
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
          <div style={{ background: 'white', padding: '1rem', borderRadius: '4px', width: '90%', maxWidth: '600px' }}>
            <Quiz selectedWord={selectedWord} summary={summaryArr[currentSummaryIndex]} onExit={closeQuizModal} />
          </div>
        </div>
      )}
    </div>
  );
};

export default SidePanel;
