import googletrans
import pandas as pd
from collections import defaultdict
import numpy as np

def back_translation(text_list, language = 'random'):

    languages = list(googletrans.LANGUAGES.keys())
    
    translator = googletrans.Translator()

    if language == 'random':
        num = 2
    else:
        num = 1
        if language not in languages:
            print (googletrans.LANGUAGES)
            raise Exception('Please select a valid language from above')
    
    df_back = pd.DataFrame(columns = ['Original', 'Back Translated', 'Random Language'])
    per = defaultdict(list)
    
    if type(text_list) == str:
        ls = []
        ls.append(text_list)
        text_list = ls
        del ls
    else:
        pass

    for text in text_list:

        detected_lang = translator.detect(text).lang
        b_2 = detected_lang

        for _ in range(num):

            if num == 2:
                rand_lang = np.random.choice([lang for lang in languages if lang not in [detected_lang, b_2]])
            else:
                rand_lang = language

            random_translation = translator.translate(text, dest = rand_lang).text

            back_translation = translator.translate(random_translation, dest = detected_lang).text

            if back_translation != text:
                break
          
            b_2 = rand_lang

        per['Original'].append(text)
        per['Back Translated'].append(back_translation)
        per['Random Language'].append(rand_lang)

    df_back['Original'] = per['Original']
    df_back['Back Translated'] = per['Back Translated']
    df_back['Random Language'] = per['Random Language']

    return df_back