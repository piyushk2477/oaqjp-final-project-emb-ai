"use strict";

function RunSentimentAnalysis() {
    const input = document.getElementById("textToAnalyze");
    const output = document.getElementById("system_response");
    const text = input.value.trim();

    if (!text) {
        output.textContent = "Please enter some text to analyze.";
        return;
    }

    output.textContent = "Analyzing...";
    fetch(`/emotionDetector?textToAnalyze=${encodeURIComponent(text)}`)
        .then((response) => response.text().then((body) => {
            if (!response.ok) {
                throw new Error(body || "The request failed.");
            }
            return body;
        }))
        .then((result) => {
            output.textContent = result;
        })
        .catch((error) => {
            output.textContent = error.message || "Unable to analyze the text.";
        });
}
