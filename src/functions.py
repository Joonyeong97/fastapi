import numpy as np
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import re

model_name = 'joon09/kor-naver-ner-name'

class NerModel:
    def __init__(self, model_name, max_len=256):
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForTokenClassification.from_pretrained(model_name)
        self.ner = pipeline("ner", model=model, tokenizer=tokenizer)
        self.max_len = max_len

    def _get_ner_tag(self, text):
        return self.ner(text)

    def _subtract_index(self, index: list):
        return np.abs(index[0] - index[1])

    def _get_split_max_len_text(self, text):
        split_strings = []
        for index in range(0, len(text), self.max_len):
            split_strings.append(text[index: index + self.max_len])

        return split_strings

    def __call__(self, *args, **kwargs):

        raise ''


class Ner(NerModel):

    def get_max_len_process(self, split_strings):
        ner_tags = []
        for text in split_strings:
            ner_tag = self._get_ner_tag(text)
            ner_tags.extend(ner_tag)

        return ner_tags

    def __call__(self, text):
        input_text = ' '.join(text.split())
        if len(input_text) > self.max_len:
            split_strings = self._get_split_max_len_text(input_text)
            max_len_processed = self.get_max_len_process(split_strings)

        else:
            max_len_processed = self._get_ner_tag(text)

        return max_len_processed