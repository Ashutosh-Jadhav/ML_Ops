import pytest
import sys
from unittest.mock import MagicMock

# Create a mock for the entire transformers module
mock_transformers = MagicMock()

mock_auto_model = MagicMock()
mock_auto_model.from_pretrained = MagicMock(return_value=MagicMock())

mock_auto_tokenizer = MagicMock()
mock_auto_tokenizer.from_pretrained = MagicMock(return_value=MagicMock())

mock_qa_function = MagicMock(return_value={"answer": "mocked answer", "score": 0.95})

mock_transformers.AutoModelForQuestionAnswering = mock_auto_model
mock_transformers.AutoTokenizer = mock_auto_tokenizer
mock_transformers.pipeline = MagicMock(return_value=mock_qa_function)

sys.modules['transformers'] = mock_transformers

from qna_service import app, QARequest
print("Successfully imported from qna_service.py")


# Now import TestClient for testing the API
from fastapi.testclient import TestClient

# Create a test client
client = TestClient(app)

# Test cases
def test_valid_qa_request():
    """Test a valid question and context request"""
    response = client.post(
        "/answer",
        json={"question": "What is FastAPI?", "context": "FastAPI is a modern web framework for building APIs with Python."}
    )
    
    # Check response
    assert response.status_code == 200
    assert response.json() == {"answer": "mocked answer"}

def test_empty_question():
    """Test error handling when question is empty"""
    response = client.post(
        "/answer",
        json={"question": "", "context": "Some context"}
    )
    
    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == "Both 'question' and 'context' are required"

def test_empty_context():
    """Test error handling when context is empty"""
    response = client.post(
        "/answer",
        json={"question": "What is FastAPI?", "context": ""}
    )
    
    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == "Both 'question' and 'context' are required"

def test_missing_question():
    """Test error handling when question is missing"""
    response = client.post(
        "/answer",
        json={"context": "Some context"}
    )
    
    assert response.status_code == 422  # FastAPI validation error
    assert "detail" in response.json()

def test_missing_context():
    """Test error handling when context is missing"""
    response = client.post(
        "/answer",
        json={"question": "What is FastAPI?"}
    )
    
    assert response.status_code == 422  # FastAPI validation error
    assert "detail" in response.json()

def test_invalid_json():
    """Test error handling for invalid JSON"""
    response = client.post(
        "/answer",
        data="This is not JSON"
    )
    
    assert response.status_code == 422  # FastAPI validation error

@pytest.mark.parametrize(
    "question,context",
    [
        ("Who created Python?", "Python was created by Guido van Rossum in the late 1980s."),
        ("When was Python created?", "Python was created by Guido van Rossum in the late 1980s."),
    ]
)
def test_different_questions(question, context):
    """Test different question/context pairs"""
    response = client.post(
        "/answer",
        json={"question": question, "context": context}
    )
    
    assert response.status_code == 200
    assert response.json() == {"answer": "mocked answer"}

def test_long_context():
    """Test with a very long context"""
    long_context = "This is a very long context. " * 100  # Repeat to make it long
    
    response = client.post(
        "/answer",
        json={"question": "What is this?", "context": long_context}
    )
    
    assert response.status_code == 200
    assert response.json() == {"answer": "mocked answer"}