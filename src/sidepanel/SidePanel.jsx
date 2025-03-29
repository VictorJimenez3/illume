import React, { useEffect, useState } from 'react';
import Quiz from '../quiz/Quiz';
import { fetchSummary } from '../api_helpers';

// A helper to wrap chrome.storage.local.get in a promise.
const getStorageValue = (key) => {
  return new Promise((resolve) => {
    chrome.storage.local.get(key, (result) => resolve(result[key]));
  });
};

const SidePanel = () => {
  const [selectedWord, setSelectedWord] = useState('');
  const [summary, setSummary] = useState('');
  const [detailedExplanation, setDetailedExplanation] = useState('');
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
          setSummary(data.general_explanation);
          if (data.detailed_explanation) {
            chrome.storage.local.set({ detailedExplanation: data.detailed_explanation });
            setDetailedExplanation(data.detailed_explanation);
          }
        } catch (error) {
          console.error("Error fetching summary:", error);
        }
      } else {
        setSummary("No summary selected");
      }
    };

    fetchAndDisplaySummary();
  }, []);

  const openQuizModal = () => {
    setShowQuiz(true);
  };

  const closeQuizModal = () => {
    setShowQuiz(false);
  };

  const toggleDetailed = () => {
    setShowDetailed(!showDetailed);
  };

  return (
    <div style={{ padding: '1rem', fontFamily: 'sans-serif', position: 'relative' }}>
      <h2>illume</h2>
      <p>{selectedWord || "No word selected."}</p>
      <p>{summary || `Fetching summary for ${selectedWord}...`}</p>

      {/* Toggle detailed explanation button on its own line */}
      <div style={{ marginTop: '1rem' }}>
        <button onClick={toggleDetailed}>
          {showDetailed ? "Hide Contextualized Explanation" : "Contextualize Now!"} 
        </button>
      </div>

      {showDetailed && (
        <div style={{ marginTop: '1rem' }}>
          <p>{detailedExplanation || "No contextualized explanation available."}</p>
        </div>
      )}

      {/* Open Quiz button on its own line */}
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
            <Quiz onExit={closeQuizModal} />
          </div>
        </div>
      )}
    </div>
  );
};

export default SidePanel;

// export state variables
export const getSelectedWord = () => selectedWord;
export const getSummary = () => summary;
