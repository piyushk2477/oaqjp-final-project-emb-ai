"""Unit tests for the emotion detector."""

import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Test response parsing and invalid-input handling."""

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_dominant_joy(self, mock_post):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "emotionPredictions": [{"emotion": {
                "anger": 0.01, "disgust": 0.02, "fear": 0.03,
                "joy": 0.90, "sadness": 0.04
            }}]
        }
        mock_post.return_value = response
        result = emotion_detector("I am very happy today")
        self.assertEqual(result["dominant_emotion"], "joy")
        self.assertEqual(result["joy"], 0.90)

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_dominant_anger(self, mock_post):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "emotionPredictions": [{"emotion": {
                "anger": 0.80, "disgust": 0.02, "fear": 0.03,
                "joy": 0.10, "sadness": 0.05
            }}]
        }
        mock_post.return_value = response
        self.assertEqual(
            emotion_detector("I am furious")["dominant_emotion"], "anger"
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_empty_text_does_not_call_service(self, mock_post):
        result = emotion_detector("   ")
        self.assertIsNone(result["dominant_emotion"])
        mock_post.assert_not_called()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400_returns_none_values(self, mock_post):
        response = Mock()
        response.status_code = 400
        mock_post.return_value = response
        result = emotion_detector("invalid input")
        self.assertIsNone(result["dominant_emotion"])
        self.assertIsNone(result["joy"])


if __name__ == "__main__":
    unittest.main()
