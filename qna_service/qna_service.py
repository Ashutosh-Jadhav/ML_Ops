from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer

# Define request schema
class QARequest(BaseModel):
    question: str
    context: str

# Initialize FastAPI app
app = FastAPI()

model_path = "/mnt/qna_model"  
model = AutoModelForQuestionAnswering.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
question_answerer = pipeline("question-answering", model=model, tokenizer=tokenizer)

# @app.get("/")
# def read_root():
#     return {"message": "QA Service is running. Use POST /answer for questions."}

@app.post("/answer")
def get_answer(request: QARequest):
    if not request.question or not request.context:
        raise HTTPException(status_code=400, detail="Both 'question' and 'context' are required")

    result = question_answerer(question=request.question, context=request.context)
    return {"answer": result['answer']}
