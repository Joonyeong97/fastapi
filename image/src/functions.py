from transformers import BertTokenizerFast

tokenizer = BertTokenizerFast.from_pretrained('kykim/bert-kor-base')

def tokenize(text):

    return tokenizer.tokenize(text)