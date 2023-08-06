
def number_detect(letter):
    """Detect the nature of letter is number or not"""

    try:
        int(letter)
        return True
    except:
        return False

def collab_words_in_list(list):
    """collab word into strings"""
    return ''.join(list)