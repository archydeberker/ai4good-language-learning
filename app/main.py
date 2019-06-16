import logging
import os

import numpy as np
import requests
import spacy

logger = logging.getLogger('translation_backed')
logger.setLevel(logging.DEBUG)

nlp = spacy.load('/Users/archy/anaconda/envs/translation/lib/python3.5/site-packages/en_core_web_sm/en_core_web_sm-2.1.0')

API_KEY = os.getenv('YANDEX_API_KEY')

def setup_wordlists():
    directory = "words/"
    data = {}
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            print(os.path.join(directory, filename))
            with open(os.path.join(directory, filename), encoding="ISO-8859-1") as f:
                data[filename[0:-4]] = f.read().split("Ê\n")
            continue
        else:
            continue

    words_to_difficulty = {}
    for level, words in data.items():
        level_int = int(level.split()[-1])
        for word in words:
            words_to_difficulty[word] = level_int

    return words_to_difficulty


def get_word_level(chunk, words_to_difficulty, aggregator=np.nanmean):
    out = []
    for word in chunk['text'].split():
        out.append(words_to_difficulty.get(word.strip(), np.nan))

    if len(out) > 1:
        return aggregator(out)
    elif len(out) == 1:
        return out[0]
    else:
        return None


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
        concatenated = '\n'.join(input)
        return concatenated.strip()


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


def assess_difficulty(parsed_text, words_to_difficulty):
    """

    Parameters
    ----------
    parsed_text: array containing text parsed into potentially translatable chunks

    Returns
    -------
    graded_parsed_text: array of text supplemented by difficulty scores

    """

    for chunk in parsed_text:
        if chunk['to_translate']: # eligible for translation
            level = get_word_level(chunk, words_to_difficulty)
            if level is not None:
                chunk['to_translate'] = level
            else:
                chunk['to_translate'] = 20

    # For now, let's return everything with to_translate left as true
    return parsed_text


def translate(graded_parsed_text, score_threshold=1):
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
        if chunk['to_translate'] > (20 - score_threshold):
            translated_text = get_translation(chunk['text'])
            output.append(_add_chunk(translated_text, chunk['text']))
        else:
            output.append(_add_chunk(chunk['text'], None))
            if chunk['to_translate']:
                logger.warning("Not translating %s because its too hard for user of level %d"%(chunk['text'],
                                                                                            score_threshold))

    return output


def read_dummy_data():
    with open('../test-doc.txt') as f:
        output = f.readlines()

    return output


def main(input=None, user_level=1):
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
        text = input['text']
        source = input['source']

        # Ultimately, we'd like to learn this threshold and adjust over time
        user_level = input['level']
    else:
        input = dict()
        input['text'] = read_dummy_data()
        input['source'] = 'html'
        input['level'] = user_level

    words_to_difficulty = setup_wordlists()
    processed_text = process_raw_input(input['text'], input['source'])

    logger.info('Parsing text')
    parsed_text = parse_text(processed_text)

    logger.info('Assessing difficulty')

    # Takes in series of text chunks with translatability tagged, then assign numerical score to each chunk for eventual
    # thresholding
    graded_parsed_text = assess_difficulty(parsed_text, words_to_difficulty)

    logger.info('Translating text')
    translated_text = translate(graded_parsed_text, score_threshold=input['level'])

    logger.info(translated_text)

    return translated_text


if __name__ == '__main__':
    main(user_level=19)
