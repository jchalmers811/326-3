__author__ = "James Chalmers"
__copyright__ = "Copyright 2018, 326 Project"
__credits__ = ["James Chalmers"]

__version__ = "1.0.1"
__email__ = "jchalmers811@gmail.com"
__status__ = "Test"


import sys

INVALID = "invalid sentence" # returned if sentence is deemed invalid at anypoint

def getVerbFuture(word):
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
    return verbDictionary.get(word, "invalid verb \"" + word + "\"") # default: returns invalid "verb" message

def getVerbPresent(word):
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
    return verbDictionary.get(word, "invalid verb \"" + word + "\"") # default: returns invalid "verb" message

def getVerbPastOrPresent(word):
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
    return verbDictionary.get(word, "invalid verb \"" + word + "\"") # default: returns invalid "verb" message

def getYouPronoun:


def getTheyPronoun:


def getWePronoun:


def translate(line):
    line = line.lower() # convert enlgish sentence to lowercase
    englishWords = line.split() # split line into words for processing
    maoriWords = []  # create list for maori sentence

    if len(englishWords) >= 2 and len(englishWords) <= 5: # check for invalid sentences size
        currentWord = englishWords.pop(0)

        if currentWord == "i":
            maoriWords.append("au")
            currentWord = englishWords.pop(0)

        elif currentWord == "he" or currentWord == "she":
            maoriWords.append("ia")
            currentWord = englishWords.pop(0)

        elif currentWord == "you":

            currentWord = englishWords.pop(0)
            if len(englishWords) > 2: # check sentence is long enough for inclusive/exclusive check and verb
                if currentWord == "(3" and englishWords[0] == "incl)":
                    maoriWords.append("koutou")
                    englishWords.pop(0)
                    currentWord = englishWords.pop(0)
                elif currentWord == "(2" and englishWords[0] == "incl)":
                    maoriWords.append("kōrua")
                    englishWords.pop(0)
                    currentWord = englishWords.pop(0)
                elif currentWord == "(1" and englishWords[0] == "incl)":
                    maoriWords.append("koe")
                    englishWords.pop(0)
                    currentWord = englishWords.pop(0)
            else:
                maoriWords.append("koe") # default is to assume singular inclusive you

        elif currentWord == "they":

            currentWord = englishWords.pop(0)
            if len(englishWords) > 2:  # check sentence is long enough for inclusive/exclusive check and verb
                if currentWord == "(3" and englishWords[0] == "excl)":
                    maoriWords.append("rātou")
                    englishWords.pop(0)
                    currentWord = englishWords.pop(0)
                elif currentWord == "(2" and englishWords[0] == "excl)":
                    maoriWords.append("rāua")
                    englishWords.pop(0)
                    currentWord = englishWords.pop(0)
            else:
                maoriWords.append("rāua")  # default is to assume two exclusive they

        elif currentWord == "we":

            currentWord = englishWords.pop(0)
            if len(englishWords) > 2:  # check sentence is long enough for inclusive/exclusive check and verb
                if currentWord == "(3":

                    currentWord = englishWords.pop(0)
                    if currentWord == "excl)":
                        maoriWords.append("mātou")
                        currentWord = englishWords.pop(0)
                    elif currentWord == "incl)":
                        maoriWords.append("tātou")
                        currentWord = englishWords.pop(0)
                    else:
                        return INVALID

                elif currentWord == "(2":

                    currentWord = englishWords.pop(0)
                    if currentWord == "excl)":
                        maoriWords.append("māua")
                        currentWord = englishWords.pop(0)
                    elif currentWord == "incl)":
                        maoriWords.append("tāua")
                        currentWord = englishWords.pop(0)
                    else:
                        return INVALID

            else:
                maoriWords.append("māua")  # default is to assume two exclusive we

        else:
            return INVALID

        if len(englishWords) == 1: # one left in list means auxiliary verb + verb

            if currentWord == "am" or currentWord == "are":
                maoriVerb = getVerbPresent(englishWords.pop(0))

                if "invalid verb" in maoriVerb:  # if verb was invalid return message and end early
                    return maoriVerb
                else:
                    maoriWords.insert(0, maoriVerb)
                    return ' '.join(maoriWords)

            elif currentWord == "will":
                maoriVerb = getVerbFuture(englishWords[-1])

                if "invalid verb" in maoriVerb:  # if verb was invalid return message and end early
                    return maoriVerb
                else:
                    maoriWords.insert(0, maoriVerb)
                    return ' '.join(maoriWords)

            else:
                return INVALID

        elif len(englishWords) == 0: # empty list means no auxiliary verb
            maoriVerb = getVerbPastOrPresent(currentWord)

            if "invalid verb" in maoriVerb:  # if verb was invalid return message and end early
                return maoriVerb
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

# print(translate("We (2 excl) are going"))