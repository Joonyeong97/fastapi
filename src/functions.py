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
# {
#     "text": "When SARS-CoV-2 concentrations in wastewater were normalized and compared with COVID-19 incidences, the differences between neighborhoods of varying demographics were reduced as compared to differences observed when comparing non-normalized SARS-CoV-2 with COVID-19 cases.",
#     "entities": [
#         {
#             "entity": "Virus-B",
#             "score": 0.9992361068725586,
#             "index": 2,
#             "word": "SA",
#             "start": 5,
#             "end": 7
#         },
#         {
#             "entity": "Virus-B",
#             "score": 0.9981411695480347,
#             "index": 3,
#             "word": "##RS",
#             "start": 7,
#             "end": 9
#         },
#         {
#             "entity": "Virus-I",
#             "score": 0.5094661712646484,
#             "index": 4,
#             "word": "-",
#             "start": 9,
#             "end": 10
#         },
#         {
#             "entity": "Virus-I",
#             "score": 0.9272067546844482,
#             "index": 5,
#             "word": "Co",
#             "start": 10,
#             "end": 12
#         },
#         {
#             "entity": "Virus-I",
#             "score": 0.584111750125885,
#             "index": 6,
#             "word": "##V",
#             "start": 12,
#             "end": 13
#         },
#         {
#             "entity": "Virus-I",
#             "score": 0.9995808005332947,
#             "index": 7,
#             "word": "-",
#             "start": 13,
#             "end": 14
#         },
#         {
#             "entity": "Virus-I",
#             "score": 0.9998695850372314,
#             "index": 8,
#             "word": "2",
#             "start": 14,
#             "end": 15
#         },
#         {
#             "entity": "Action-B",
#             "score": 0.8669586777687073,
#             "index": 36,
#             "word": "reduced",
#             "start": 167,
#             "end": 174
#         },
#         {
#             "entity": "Virus-B",
#             "score": 0.8437488079071045,
#             "index": 48,
#             "word": "SA",
#             "start": 241,
#             "end": 243
#         },
#         {
#             "entity": "Virus-B",
#             "score": 0.9475386738777161,
#             "index": 49,
#             "word": "##RS",
#             "start": 243,
#             "end": 245
#         },
#         {
#             "entity": "Virus-I",
#             "score": 0.9962312579154968,
#             "index": 50,
#             "word": "-",
#             "start": 245,
#             "end": 246
#         },
#         {
#             "entity": "Virus-I",
#             "score": 0.9952365756034851,
#             "index": 51,
#             "word": "Co",
#             "start": 246,
#             "end": 248
#         },
#         {
#             "entity": "Virus-I",
#             "score": 0.8436189889907837,
#             "index": 52,
#             "word": "##V",
#             "start": 248,
#             "end": 249
#         },
#         {
#             "entity": "Virus-I",
#             "score": 0.9985949397087097,
#             "index": 53,
#             "word": "-",
#             "start": 249,
#             "end": 250
#         },
#         {
#             "entity": "Virus-I",
#             "score": 0.999370276927948,
#             "index": 54,
#             "word": "2",
#             "start": 250,
#             "end": 251
#         }
#     ],
#     "text_tag": "When <Virus>SA</Virus><Virus>RS</Virus><Virus>-</Virus><Virus>Co</Virus><Virus>V</Virus><Virus>-</Virus><Virus>2</Virus> concentrations in wastewater were normalized and compared with COVID-19 incidences, the differences between neighborhoods of varying demographics were <Action>reduced</Action> as compared to differences observed when comparing non-normalized <Virus>SA</Virus><Virus>RS</Virus><Virus>-</Virus><Virus>Co</Virus><Virus>V</Virus><Virus>-</Virus><Virus>2</Virus> with COVID-19 cases."
# }

class Ner(NerModel):

    def add_length_str(self, ner_tag, index):
        if ner_tag:
            for tag in ner_tag:
                tag['start'] = (self.max_len * index) + tag['start']
                tag['end'] = (self.max_len * index) + tag['end']
        return ner_tag

    def get_max_len_process(self, split_strings):
        ner_tags = []

        for i, text in enumerate(split_strings):
            ner_tag = self._get_ner_tag(text)
            ner_tag = self.add_length_str(ner_tag, i)
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