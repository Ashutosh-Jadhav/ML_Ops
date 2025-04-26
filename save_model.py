from transformers import AutoModelForQuestionAnswering, AutoTokenizer
model_checkpoint = "ashutoshj01/bert-finetuned-squad"
model = AutoModelForQuestionAnswering.from_pretrained(model_checkpoint)
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

# saving to local dir

model.save_pretrained("./qna_model")
tokenizer.save_pretrained("./qna_model")
