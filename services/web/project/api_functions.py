from mrakun import RakunDetector

def extract_keywords(text, args):
    """
    A simple wrapper for RaKUn
    
    :param text: Input text (a string)
    :param args: The hyperparameters
    :return list: A list of top k keywords.
    """
    
    keyword_detector = RakunDetector(args)
    
    keywords = keyword_detector.find_keywords(text, input_type = "text")
    
    return [x[0] for x in keywords]
                                   
