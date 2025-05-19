from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer

model_path = "/mnt/model"
model = AutoModelForQuestionAnswering.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

question_answerer = pipeline("question-answering", model=model, tokenizer=tokenizer)

def answer_question(question, context):
    result = question_answerer(question=question, context=context)
    return result['answer']

if __name__ == "__main__":
    q = "What is the capital of France?"
    c = "Paris is the capital city of France and a major European hub."
    print(answer_question(q, c))


