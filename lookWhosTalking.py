__author__ = "James Chalmers"
__copyright__ = "Copyright 2018, 326 Project"
__credits__ = ["James Chalmers"]

__version__ = "1.0.1"
__email__ = "jchalmers811@gmail.com"
__status__ = "Test"


import sys

# constants
INVALID = "invalid sentence" # returned if sentence is deemed invalid at anypoint


def getYouPronoun(currentWord, englishWords):
    """Takes currentWord and englishWord and returns updated
    versions of both and the appropriate maori pronoun as a tuple"""

    # check sentence is long enough for inclusive/exclusive check
    if len(englishWords) > 1:
        if englishWords[0] == "(3" and englishWords[1] == "incl)":
            del englishWords[0:2]
            currentWord = englishWords.pop(0)
            return currentWord, englishWords, "koutou"
        elif englishWords[0] == "(2" and englishWords[1] == "incl)":
            del englishWords[0:2]
            currentWord = englishWords.pop(0)
            return currentWord, englishWords, "kōrua"
        elif englishWords[0,1] == "(1" and englishWords[1] == "incl)":
            del englishWords[0:2]
            currentWord = englishWords.pop(0)
            return currentWord, englishWords, "koe"

    currentWord = englishWords.pop(0)
    return currentWord, englishWords, "koe" #  will default to singular inclusive you

def getTheyPronoun(currentWord, englishWords):
    """Takes currentWord and englishWord and returns updated
    versions of both and the appropriate maori pronoun as a tuple"""

    # check sentence is long enough for inclusive/exclusive check
    if len(englishWords) > 1:
        if englishWords[0] == "(3" and englishWords[1] == "excl)":
            del englishWords[0:2]
            currentWord = englishWords.pop(0)
            return currentWord, englishWords, "rātou"
        elif englishWords[0] == "(2" and englishWords[1] == "excl)":
            del englishWords[0:2]
            currentWord = englishWords.pop(0)
            return currentWord, englishWords, "rāua"

    currentWord = englishWords.pop(0)
    return currentWord, englishWords, "rāua"  # default is to assume two exclusive they

def getWePronoun(currentWord, englishWords):
    """Takes currentWord and englishWord and returns updated
    versions of both and the appropriate maori pronoun as a tuple"""

    # check sentence is long enough for inclusive/exclusive check
    if len(englishWords) > 1:

        if englishWords[0] == "(3":
            if englishWords[1] == "excl)":
                del englishWords[0:2]
                currentWord = englishWords.pop(0)
                return currentWord, englishWords, "mātou"
            elif englishWords[1] == "incl)":
                del englishWords[0:2]
                currentWord = englishWords.pop(0)
                return currentWord, englishWords, "tātou"

        elif englishWords[0] == "(2":
            if englishWords[1] == "excl)":
                del englishWords[0:2]
                currentWord = englishWords.pop(0)
                return currentWord, englishWords, "māua"
            elif englishWords[0] == "incl)":
                del englishWords[0:2]
                currentWord = englishWords.pop(0)
                return currentWord, englishWords, "tāua"

    currentWord = englishWords.pop(0)
    return currentWord, englishWords, "māua" # default is to assume two exclusive we

def getVerbFuture(word):
    """Takes a word and returns the appropriate maori
    verb or None if it is invalid"""

    verbDictionary = {
        "go": "Ka haere",
        "make": "Ka hanga",
        "see": "Ka kite",
        "want": "Ka hiaia",
        "call": "Ka karanga",
        "ask": "Ka pātai",
        "read": "Ka pānui",
        "learn": "Ka ako"
    }
    return verbDictionary.get(word, None) # default: returns invalid "verb" message

def getVerbPresent(word):
    """Takes a word and returns the appropriate maori
    verb or None if it is invalid"""

    verbDictionary = {
        "going": "Kei te haere",
        "making": "Kei te hanga",
        "seeing": "Kei te kite",
        "wanting": "Kei te hiaia",
        "calling": "Kei te karanga",
        "asking": "Kei te pātai",
        "reading": "Kei te pānui",
        "learning": "Kei te ako"
    }
    return verbDictionary.get(word, None) # default: returns invalid "verb" message

def getVerbPastOrPresent(word):
    """Takes a word and returns the appropriate maori
    verb or None if it is invalid"""

    verbDictionary = {
        "go": "Kei te haere",
        "make": "Kei te hanga",
        "see": "Kei te kite",
        "want": "Kei te hiaia",
        "call": "Kei te karanga",
        "ask": "Kei te pātai",
        # read defaults to past tense below
        "learn": "Kei te ako",
        "went": "I haere",
        "made": "I hanga",
        "saw": "I kite",
        "wanted": "I hiaia",
        "called": "I karanga",
        "asked": "I pātai",
        "read": "I pānui", # read defaults to past tense
        "learned": "I ako"
    }
    return verbDictionary.get(word, None) # default: returns invalid "verb" message



def translate(line):
    """Processes each english sentence and returns INVALID or maori sentence"""

    line = line.lower() # convert enlgish sentence to lowercase
    englishWords = line.split() # split line into words for processing, write to global variable
    maoriWords = []      # create list for maori sentence

    # check for valid sentences size before popping
    if len(englishWords) >= 2 and len(englishWords) <= 5:
        currentWord = englishWords.pop(0)

        # check for simple pronouns in main function
        if currentWord == "i":
            maoriWords.append("au")
            currentWord = englishWords.pop(0)

        elif currentWord == "he" or currentWord == "she":
            maoriWords.append("ia")
            currentWord = englishWords.pop(0)

        # check for more complex pronouns with methods

        elif currentWord == "you":
            currentWord, englishWords, maoriPronoun = getYouPronoun(currentWord, englishWords)
            maoriWords.append(maoriPronoun)

        elif currentWord == "they":
            currentWord, englishWords, maoriPronoun = getTheyPronoun(currentWord, englishWords)
            maoriWords.append(maoriPronoun)

        elif currentWord == "we":
            currentWord, englishWords, maoriPronoun = getWePronoun(currentWord, englishWords)
            maoriWords.append(maoriPronoun)

        else:
            return INVALID


        # infer tense and get verb
        # one left in list means auxiliary verb + verb
        if len(englishWords) == 1:

            if currentWord == "am" or currentWord == "are" or currentWord == "is":
                currentWord = englishWords.pop(0)
                maoriVerb = getVerbPresent(currentWord)

                # if verb was invalid return message and end early
                if maoriVerb == None:
                    return "invalid verb \"" + currentWord + "\""
                else:
                    maoriWords.insert(0, maoriVerb)
                    return ' '.join(maoriWords)

            elif currentWord == "will":
                currentWord = englishWords.pop(0)
                maoriVerb = getVerbFuture(currentWord)

                # if verb was invalid return message and end early
                if maoriVerb == None:
                    return "invalid verb \"" + currentWord + "\""
                else:
                    maoriWords.insert(0, maoriVerb)
                    return ' '.join(maoriWords)

            else:
                return INVALID

        # empty list means no auxiliary verb
        elif len(englishWords) == 0:
            maoriVerb = getVerbPastOrPresent(currentWord)

            if maoriVerb == None:  # if verb was invalid return message and end early
                return "invalid verb \"" + currentWord + "\""
            else:
                maoriWords.insert(0, maoriVerb)
                return ' '.join(maoriWords)


        else:
            return INVALID

    else:
        return INVALID


# read lines from stdin one at a time
for line in sys.stdin:
     print(translate(line))



