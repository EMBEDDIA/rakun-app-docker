from mrakun import RakunDetector

def extract_keywords(text, args):
    """
    A simple wrapper for RaKUn
    
    :param text: Input text (a string)
    :param args: The hyperparameters
    :return list: A list of top k keywords.
    """

    ## Initialize the extractor
    keyword_detector = RakunDetector(args)

    ## Find the keywords
    keywords = keyword_detector.find_keywords(text, input_type = "text")

    ## Return the keyword list
    return [x[0] for x in keywords]
