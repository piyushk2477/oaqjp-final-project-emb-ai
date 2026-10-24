"""Detect emotions in text using the IBM Watson NLP emotion model."""

import requests

NLP_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"
EMOTION_KEYS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text):
    """Return emotion scores and the dominant emotion for *text*.

    If the service rejects the input (for example, an empty string), return
    a dictionary whose emotion values and dominant_emotion are None.
    """
    if not isinstance(text, str) or not text.strip():
        return {**dict.fromkeys(EMOTION_KEYS), "dominant_emotion": None}

    headers = {"grpc-metadata-mm-model-id": MODEL_ID}
    payload = {"raw_document": {"text": text}}

    try:
        response = requests.post(
            NLP_URL, json=payload, headers=headers, timeout=30
        )
        if response.status_code == 400:
            return {**dict.fromkeys(EMOTION_KEYS), "dominant_emotion": None}
        response.raise_for_status()
        prediction = response.json()["emotionPredictions"][0]["emotion"]
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
        return {**dict.fromkeys(EMOTION_KEYS), "dominant_emotion": None}

    scores = {key: prediction.get(key) for key in EMOTION_KEYS}
    available_scores = {
        key: value for key, value in scores.items() if isinstance(value, (int, float))
    }
    dominant = max(available_scores, key=available_scores.get) if available_scores else None
    return {**scores, "dominant_emotion": dominant}
