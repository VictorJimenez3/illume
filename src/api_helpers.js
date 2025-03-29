// src/helpers/api.js
import { API_BASEURL } from "./config.js";

export async function fetchSummary(keyword, siteText) {
  const requestBody = {
    keyword,
    data: siteText || ""
  };

  console.log("making the request");
  const response = await fetch(`${API_BASEURL}/makeSummary`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(requestBody)
  });

  if (!response.ok) {
    throw new Error(`API call failed with status ${response.status}`);
  }

  console.log("response received and parsing into json");


  const json = await response.json();
  return json;
}


export async function fetchQuestions(keyword, explanation) {
    const requestBody = {
        keyword,
        explanation
    };
    const response = await fetch(`${API_BASEURL}/makeQuestions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody)
    });
    if (!response.ok) {
        throw new Error(`Error fetching questions: ${response.statusText}`);
    }
    return await response.json();
}
