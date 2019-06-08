def process_raw_input(input, type='html'):
    """

    Parameters
    ----------
    input
    type

    Returns
    -------
    processed text (str)
    """
    pass


def parse_text(text_input):
    """
    Parameters
    ----------
    input

    Returns
    -------
    parsed_text: an array with potential translations tagged

    """
    pass


def assess_difficulty(parsed_text):
    """

    Parameters
    ----------
    parsed_text: array containing text parsed into potentially translatable chunks

    Returns
    -------
    graded_parsed_text: array of text supplemented by difficulty scores

    """
    pass


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

    pass


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
    text = input['text']
    source = input['source']

    # Ultimately, we'd like to learn this threshold and adjust over time
    user_level = input['level']

    processed_text = process_raw_input(text, source)
    parsed_text = parse_text(processed_text)
    graded_parsed_text = assess_difficulty(parsed_text)

    translated_text = translate(graded_parsed_text, score_threshold=user_level)

    return translated_text

