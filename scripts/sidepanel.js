document.addEventListener("DOMContentLoaded", async () => {
    const { selectedText } = await chrome.storage.local.get("selectedText");
    await chrome.storage.local.set({inQuiz: false});
    document.getElementById("selected-topic").textContent = selectedText || "Nothing selected.";
});

document.addEventListener("DOMContentLoaded", () => {
    chrome.storage.local.get("selectedText", async (result) => {
      const word = result.selectedText;
      const outputElem = document.getElementById("output");
      
      if (word) {
        outputElem.textContent = `Fetching definition for "${word}"...`;
        
        try {

          // INSERT API ENDPOINT
          const response = await fetch(`https://amazon.com`);
          
          if (response.ok) {
            const json = await response.json();
            outputElem.textContent = json.definition || "Definition not found."; // Expecting to have a "definition" property
          } else {
            outputElem.textContent = "Error fetching definition.";
          }
        } catch (error) {
          
          // error with making the fetch call
          outputElem.textContent = `Error: ${error.message}`;
        }
      } else {
        outputElem.textContent = getDefaultLorem();
      }
    });
  });

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('learnMoreButton').addEventListener('click', async function() {

        if(!(await chrome.storage.session.get('inQuiz'))["inQuiz"]) {
          await chrome.storage.local.set({inQuiz: true});
          
          quizWindow = window.open('quiz.html', '_blank');

          // Start polling every 500ms to check if it's closed. If it is we re-allow the opportunity to open another by changing local-storage flag
          quizPollInterval = setInterval(async () => {
            if (!quizWindow || quizWindow.closed) {
              await chrome.storage.local.set({inQuiz: false});
              console.log("Quiz window closed.");
              clearInterval(quizPollInterval);
            }
          }, 500);

        } else {
          console.log("trying to open quiz window")
        }

    });
});