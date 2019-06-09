from flask import Flask, request ,redirect,jsonify
import requests
import random
import json
import time
import os
import spacy
import requests
import os
import logging
from datetime import datetime
import en_core_web_sm


def setup_wordlists(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vocab')):
    data = {}
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
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

def update_user_json(filepath, translated_text, ip):
    with open(filepath, 'r') as fp:
        user_dict = json.load(fp)
    user_dict[ip]['most_recent_session']['translated_chunks'] = [chunk['original'] for chunk in translated_text if chunk['original'] is not None]
    with open(filepath, 'w') as fp:
        json.dump(user_dict, fp, indent=2)

def get_key(filename, key):
    f = filename
    cred = json.loads(open(f).read())
    return cred[key]

app = Flask(__name__)


@app.route('/')
def index():
    return "WELCOME TO AI4GOOD !!"


@app.route('/update-user')
def push_user_update():
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./users_level_file.json")
    user_json = json.loads(open(f).read())

    ip = request.args["ip"]
    level = request.args["level"]

    user_json[ip]['last_estimated_level'] = int(level)

    with open(f, 'w') as fp:
        json.dump(user_json, fp, indent=2)

    return jsonify(user_json)

@app.route('/user-levels')
def user_levels():
    f =os.path.join(os.path.dirname(os.path.abspath(__file__)), "./users_level_file.json")
    user_json = json.loads(open(f).read())
    return jsonify(user_json)

@app.route('/translate', methods=['GET'])
def translate():
    try:
        api_key = get_key('./Secrets/yandex_key.json', 'api_key')
    except:
        api_key = os.getenv('YANDEX_API_KEY')

    text=request.args["txt"]
    r = requests.post('https://translate.yandex.net/api/v1.5/tr.json/translate',
                      data={'key': api_key,
                            'text': text,
                            'lang': 'en-fr'})
    return jsonify(r.json())


@app.route('/query-example')
def query_example():

    def get_key(filename,key):
        f = filename
        cred = json.loads(open(f).read())
        return cred[key]

    def get_level(filename, ip):
        f = filename
        cred = json.loads(open(f).read())
        if ip not in cred:
            cred[ip] = dict(last_estimated_level=10,
                            most_recent_session=dict(translated_chunks=[],
                                                     clicked_chunks=[]))

        with open(filename, 'w') as fp:
            json.dump(cred, fp, indent=2)

        return cred[ip]['last_estimated_level']

    def get_session_info(filename, ip):
        f = filename
        cred = json.loads(open(f).read())

        return cred[ip]['most_recent_session']['translated_chunks'], cred[ip]['most_recent_session']['clicked_chunks']


    logger = logging.getLogger('translation_backed')
    logger.setLevel(logging.DEBUG)

    nlp = en_core_web_sm.load()

    try:
        API_KEY = get_key('./Secrets/yandex_key.json', 'api_key')
    except:
        API_KEY = os.getenv('YANDEX_API_KEY')

    word_to_difficulty = setup_wordlists()

    def get_translation(word):
        r = requests.post('https://translate.yandex.net/api/v1.5/tr.json/translate',
                          data={'key': API_KEY,
                                'text': word,
                                'lang': 'en-fr'})
        print(r.json())
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

    def update_level(level, read_chunks, unknown_chunks, k=1):
        expected = 0
        actual = 0
        for chunk in read_chunks:
            words = chunk.split(' ')
            chunk_level = max(word_to_difficulty.get(w, 0) for w in words)
            if chunk_level == 0:
                continue
            expected += 1 / (1 + 10**((chunk_level - level)/20))
            if chunk not in unknown_chunks:
                actual += 1
            else:
                actual -= 1

        level += k * (actual - expected)

        level = max(level, 1)

        return level

    def assess_difficulty(parsed_text, user_level, k=1):
        """

        Parameters
        ----------
        parsed_text: array containing text parsed into potentially translatable chunks

        Returns
        -------
        graded_parsed_text: array of text supplemented by difficulty scores

        """
        for chunk in parsed_text:
            if not chunk['to_translate']:
                continue

            words = chunk['text'].split(' ')
            print(words)
            chunk_levels = [word_to_difficulty.get(w, 0) for w in words if len(w) > 0]
            if not chunk_levels or sum(chunk_levels) == 0:
                chunk['to_translate'] = False
                continue

            chunk_level = max(level for level in chunk_levels)
            print(chunk)
            print(chunk_levels)
            if chunk_level > 0 and chunk_level <= user_level:
                # to_translate = (random.random() > 1/level)
                to_translate = True
                chunk['to_translate'] = to_translate
            else:
                chunk['to_translate'] = False


        return parsed_text

    def translate(graded_parsed_text):
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
        with open('./test-doc.txt') as f:
            output = f.readlines()

        return output

    def main_function(input=None,ip=None):
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
            source = input.get('source', None)

            # Check the user level from our JSON
            user_level = get_level(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./users_level_file.json"), ip)
            read_words, unknown_words = get_session_info(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./users_level_file.json"), ip)

            user_level = update_level(user_level, read_words, unknown_words)
        else:
            input = dict()
            read_words = read_dummy_data()
            input['source'] = 'html'
            user_level = 1

        processed_text = process_raw_input(text, source)

        logger.info('Parsing text')
        parsed_text = parse_text(processed_text)

        logger.info('Assessing difficulty')
        graded_parsed_text = assess_difficulty(parsed_text, user_level)

        logger.info('Translating text')
        translated_text = translate(graded_parsed_text)

        logger.info(translated_text)

        return [{"ip": ip, "user_level": user_level}], translated_text

    input = request.args
    start = time.clock()
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    now = datetime.now()
    time_taken = time.clock() - start

    user_json, translated_text = main_function(input, ip)

    # Update the user json with the new words we've translated
    update_user_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./users_level_file.json"),
                     translated_text, ip)

    translated_text = [{"timestamp": now,
                      "time_taken": time_taken,
                       "ip": ip}] + translated_text

    return jsonify(translated_text)


if __name__ == '__main__':
    app.run(debug=True,host= '127.0.0.1', port=5000) #run app in debug mode on port 5000
