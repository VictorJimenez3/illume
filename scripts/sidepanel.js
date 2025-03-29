document.addEventListener("DOMContentLoaded", async () => {
    const { selectedText } = await chrome.storage.local.get("selectedText");
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
          const response = await fetch(`http://127.0.0.1:5000/getDefinition?word=${encodeURIComponent(word)}`);
          
          if (response.ok) {
            const json = await response.json();
            // Expecting the returned JSON to have a "definition" property
            outputElem.textContent = json.definition || "Definition not found.";
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
  

  // Returns a sample Lorem Ipsum text (4-5 sentences)
function getDefaultLorem() {
    return "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus lacinia odio vitae vestibulum vestibulum. Cras venenatis euismod malesuada. Integer in ante non felis malesuada hendrerit. Proin vitae facilisis libero.";
  }