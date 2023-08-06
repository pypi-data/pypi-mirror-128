Description
--------

Back translation is the process of translating the text into a target language and then retranslating it into its source language. For example, translating the content from English to Swedish and retranslating it to English. In this process, the text retranslated to its source language from a target language might be a little different but conveys the same meaning or sentiment. </br>

In the context of NLP, it's a very useful technique for text augmentation when the text data is not enough and we need more data to train a good model. If the sentence is not the same after the back translation then we'll keep the sentence. This technique is also known as Reverse Translation. </br>

The library is designed to automate the process by taking the text data and converting it to some other language that can be chosen by the user or the library choose randomly and output the original and back-translated data. </br>

Installation
--------

```
$ pip install btranslation
```

Example
--------

#### Basic Usage
Back translating a single sentence, using Russian. If the language is not given, then the library chooses a random language other than the initial one.</br>
*Note: The output is a Data Frame.*
```
>>> import btranslation
>>> btrans = btranslation.back_translation('I drive the car very well', language = 'ru')
>>> print (btrans) 
                    Original     Back Translated Random Language
0  I drive the car very well  I drive very well.              ru
```

#### Advanced Usage (Bulk)
Back translating more than one sentence at a time.
```
>>> import btranslation
>>> btrans = btranslation.back_translation(['I drive the car very well', 'I can not ride a bicycle'], language = 'ru')
>>> print (btrans) 
                    Original     Back Translated Random Language
0  I drive the car very well  I drive very well.              ru
1  I can not ride a bicycle   I can't ride a bike             ru
```

Requirements
--------
- Python >= 3.0
