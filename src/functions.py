from transformers import BertTokenizerFast, BertForSequenceClassification, pipeline

tokenizer = BertTokenizerFast.from_pretrained('joon09/kor-naver-ner-name')
model = BertForSequenceClassification.from_pretrained('joon09/kor-naver-ner-name')
ner = pipeline('ner', model=model, tokenizer=tokenizer)

def name_tag(text):

    return ner(text)

