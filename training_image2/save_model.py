from transformers import AutoModelForQuestionAnswering, AutoTokenizer
# model_checkpoint = "ashutoshj01/bert-finetuned-squad"
model_checkpoint = "ashutoshj01/bert-finetuned-squad"
model = AutoModelForQuestionAnswering.from_pretrained(model_checkpoint)
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

model.save_pretrained("./mnt/model")
tokenizer.save_pretrained("./mnt/model")
