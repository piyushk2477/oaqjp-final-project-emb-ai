"""Flask web application for the emotion detector."""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def home():
    """Render the main page."""
    return render_template("index.html")


@app.route("/emotionDetector")
def detect_emotion():
    """Analyze the supplied text and return a readable result."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    if not text_to_analyze.strip():
        return "Please enter some text to analyze.", 400

    result = emotion_detector(text_to_analyze)
    dominant = result.get("dominant_emotion")
    if dominant is None:
        return "Unable to analyze the text. Please try again.", 502

    scores = ", ".join(
        f"'{emotion}': {result[emotion]}" 
        for emotion in ("anger", "disgust", "fear", "joy", "sadness")
    )
    return (
        f"For the given statement, the system response is {scores}. "
        f"The dominant emotion is {dominant}."
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
