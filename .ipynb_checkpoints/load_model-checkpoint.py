from transformers import pipeline

model_checkpoint = "ashutoshj01/bert-finetuned-squad"
question_answerer = pipeline("question-answering", model=model_checkpoint)

context = """
The Amazon rainforest, often referred to as the "lungs of the Earth," is the largest tropical rainforest in the world, covering over 5.5 million square kilometers. It is home to an incredibly diverse range of species, including more than 40,000 types of plants, 1,300 bird species, and 2.5 million different insects. The Amazon plays a crucial role in regulating the Earth's climate by absorbing vast amounts of carbon dioxide. However, in recent decades, deforestation caused by logging, farming, and mining activities has severely threatened the rainforest's ecosystem and biodiversity.
"""
question = "What is the Amazon rainforest often called?"
ans = question_answerer(question=question, context=context)
print(ans)