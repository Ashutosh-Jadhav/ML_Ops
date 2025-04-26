from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer

model = AutoModelForQuestionAnswering.from_pretrained("./qna_model")
tokenizer = AutoTokenizer.from_pretrained("./qna_model")

question_answerer = pipeline("question-answering", model=model, tokenizer=tokenizer)

context = """The Amazon rainforest, often referred to as the "lungs of the Earth," ..."""
question = "What is the Amazon rainforest often called?"
ans = question_answerer(question=question, context=context)
print(ans)