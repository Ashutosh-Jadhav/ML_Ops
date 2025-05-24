import argparse
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer

def answer_question(question, context):
    model_path = "/mnt/model"  
    model = AutoModelForQuestionAnswering.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    question_answerer = pipeline("question-answering", model=model, tokenizer=tokenizer)
    
    result = question_answerer(question=question, context=context)
    return result['answer']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--context", required=True)
    parser.add_argument("--question", required=True)
    args = parser.parse_args()

    answer = answer_question(args.question, args.context)
    print(answer)

if __name__ == "__main__":
    main()
