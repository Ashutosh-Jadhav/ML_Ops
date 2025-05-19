from transformers import AutoModelForQuestionAnswering, AutoTokenizer

# Load your model and tokenizer
model = AutoModelForQuestionAnswering.from_pretrained("./qna_model")
tokenizer = AutoTokenizer.from_pretrained("./qna_model")

# Push model to Hub
model.push_to_hub("ashutoshj01/bert-finetube-squad")  # e.g., "john-doe/amazon-qa-model"
tokenizer.push_to_hub("ashutoshj01/bert-finetube-squad")
