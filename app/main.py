import spacy
import requests
import os



nlp = spacy.load('/Users/archy/anaconda/envs/translation/lib/python3.5/site-packages/en_core_web_sm/en_core_web_sm-2.1.0')


def get_translation(word):
    r = requests.post('https://translate.yandex.net/api/v1.5/tr.json/translate',
                      data={'key': api_key,
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


def _add_chunk(text, original_text=None):
    return dict(text=text,
                original=original_text)

def _to_translate_wrapper(text, to_translate=True)
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
            print(token.text_with_ws)
        elif token.pos_ == 'NOUN' or token.pos_ == 'PROPN':
            if len(trace) > 0:
                trace.append(token.text_with_ws)
                print('translating', trace)
                output_array.append(_to_translate_wrapper(' '.join(trace), True))
                trace = []
                print('___')
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

    for chunk in graded_parsed_text:
        if item['to_translate']:

def read_dummy_data():
    with open('hod-raw.txt') as f:
        output = f.readlines()

    return output

def main(input):
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
        input['text'] = read_dummy_data()
        input['source'] = 'html'
        input['level'] = 1

    processed_text = process_raw_input(text, source)
    parsed_text = parse_text(processed_text)
    graded_parsed_text = assess_difficulty(parsed_text)

    translated_text = translate(graded_parsed_text, score_threshold=user_level)

    return translated_text

