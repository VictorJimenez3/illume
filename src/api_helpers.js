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



export async function fetchNewQuestions(keyword, data, wrong_questions) {
    // TODO: wrong_questions to be formatted as string
    const requestBody = {
        keyword,
        data,
        wrong_questions
    };
    const response = await fetch(`${API_BASEURL}/makeNewQuestions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody)
    });
    if (!response.ok) {
        throw new Error(`Error fetching questions: ${response.statusText}`);
    }
    return await response.json();

    /*
    expected output
    {
    questions_raw
    answers_raw
    questions
    }

    */
}


export async function fetchSummaryAdjustments(keyword, new_questions, new_answers) {
    // TODO: wrong_questions to be formatted as string
    const requestBody = {
        keyword,
        new_questions,
        new_answers
    };
    const response = await fetch(`${API_BASEURL}/makeSummaryAdjustment`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody)
    });
    if (!response.ok) {
        throw new Error(`Error fetching questions: ${response.statusText}`);
    }
    return await response.json();

    /*
    expected output
    {
    summary_adjustment
    }

    */
}



export async function fetchVideo(topic) {
    // TODO: wrong_questions to be formatted as string
    const requestBody = {
        topic
    };
    const response = await fetch(`${API_BASEURL}/youtubeVideoFinder`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody)
    });
    if (!response.ok) {
        throw new Error(`Error fetching questions: ${response.statusText}`);
    }
    return await response.json();

    /*
    expected output
    {
    title
    video_url
    }

    */
}