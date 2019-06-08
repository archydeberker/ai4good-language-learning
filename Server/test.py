import spacy
import requests
import os
import logging
import json
from pprint import pprint


def get_key():
    f = '../Server/Secrets/yandex_key.json'
    cred = json.loads(open(f).read())
    return cred['api_key']

logger = logging.getLogger('translation_backed')
logger.setLevel(logging.DEBUG)

nlp = spacy.load(r'/home/rahul/anaconda3/envs/ai4_env/lib/python3.7/site-packages/en_core_web_sm/en_core_web_sm-2.0.0/')

API_KEY = get_key()


def get_translation(word):
    r = requests.post('https://translate.yandex.net/api/v1.5/tr.json/translate',
                      data={'key': API_KEY,
                            'text': word,
                            'lang': 'en-fr'})

    return ' '.join(r.json()['text'])


def process_raw_input(input, source='html'):
    """

    Parameters
    ----------
    input
    type

    Returns
    -------
    processed text (str)
    """
    if source == 'html':
        return '\n'.join(input)
    elif source == None:
        return input


def _add_chunk(text, original_text=None):
    return dict(text=text,
                original=original_text)

def _to_translate_wrapper(text, to_translate=True):
    return dict(text=text,
                to_translate=to_translate)

def parse_text(text_input):
    """
    Parameters
    ----------
    input

    Returns
    -------
    parsed_text: an array with potential translations tagged

    """

    # Run spacy on the input document
    doc = nlp(text_input)
    output_array = []

    trace = []
    for token in doc:
        if token.pos_ == 'DET' or token.pos_ == 'ADJ':
            trace.append(token.text_with_ws)
        elif token.pos_ == 'NOUN' or token.pos_ == 'PROPN':
            if len(trace) > 0:
                trace.append(token.text_with_ws)
                output_array.append(_to_translate_wrapper(' '.join(trace), True))
                trace = []
            else:
                output_array.append(_to_translate_wrapper(token.text_with_ws, True))
        else:
            if token.pos_ == 'PUNCT' and len(trace) > 0:
                output_array.append(_to_translate_wrapper(' '.join(trace), True))
                trace = []

            output_array.append(_to_translate_wrapper(token.text_with_ws, False))

    return output_array


def assess_difficulty(parsed_text):
    """

    Parameters
    ----------
    parsed_text: array containing text parsed into potentially translatable chunks

    Returns
    -------
    graded_parsed_text: array of text supplemented by difficulty scores

    """

    # For now, let's return everything with to_translate left as true
    return parsed_text


def translate(graded_parsed_text, score_threshold=0):
    """
    Translate all chunks in graded_parsed_text for which the difficulty score is below the given threshold.

    Parameters
    ----------
    graded_parsed_text
    grade_threshold

    Returns
    -------
    translated_text: array containing dicts with text + translation
        e.g. [
              {‘text’: ‘J’ai mal a la jambe’, ‘original’:”my leg hurts”},
              {‘text’: ‘because I fell down.’, “original”:None}
              ]

    """
    output = []
    for chunk in graded_parsed_text:
        if chunk['to_translate']:
            translated_text = get_translation(chunk['text'])
            output.append(_add_chunk(translated_text, chunk['text']))
        else:
            output.append(_add_chunk(chunk['text'], None))

    return output


def read_dummy_data():
    with open('./Server/test-doc.txt') as f:
        output = f.readlines()

    return output


def main(input=None):
    """

    Parameters
    ----------
    input: dictionary containing
                text: the input text, potentially with HTML tags
                source: where it's come from (Youtube or Webpage)
                user_level: the language level of the current user

    Returns
    -------
    translated_text: list of dicts, with each dict containing
                text: text to be rendered
                original: the original form of that text. if None, it has not been translated.

    """
    if input is not None:
        text = input.get('text')
        source = input.get('source',None)

        # Ultimately, we'd like to learn this threshold and adjust over time
        user_level = input.get('level',1)
    else:
        input = dict()
        input['text'] = read_dummy_data()
        input['source'] = 'html'
        input['level'] = 1

    processed_text = process_raw_input(input.get('text'), input.get('source',None))

    logger.info('Parsing text')
    parsed_text = parse_text(processed_text)

    logger.info('Assessing difficulty')
    graded_parsed_text = assess_difficulty(parsed_text)

    logger.info('Translating text')
    translated_text = translate(graded_parsed_text, score_threshold=input.get('level',1))

    logger.info(translated_text)

    return translated_text


if __name__ == '__main__':
    output=main(input={"text":"""We left in pretty good time, and came after nightfall to Klausenburgh.
Here I stopped for the night at the Hotel Royale.

I had for dinner, or rather supper, a chicken done up some way with red pepper, which was
very good but thirsty. (_Mem._, get recipe for Mina.)"""})

    pprint(output)


