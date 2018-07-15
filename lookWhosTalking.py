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
        "read": "I pānui", # read defaults to passed tense
        "learned": "I ako"

    }
    return verbDictionary.get(word, "invalid verb \"" + word + "\"") # default: returns invalid "verb" message

def translate(line):
    line = line.lower() # convert enlgish sentence to lowercase
    englishWords = line.split() # split line into words for processing
    sentenceLength = len(englishWords) # for checking if sentence is valid
    sentencePointer = 0
    maoriWords = [] # create list for maori sentence

    if sentenceLength >= 2 and sentenceLength <= 5: # check for invalid sentences immediately

        if englishWords[sentencePointer] == "i":
            maoriWords.append("au")
            sentencePointer += 1

        elif englishWords[sentencePointer] == "he" or englishWords[sentencePointer] == "she":
            maoriWords.append("ia")
            sentencePointer += 1

        elif englishWords[sentencePointer] == "you":

            sentencePointer += 1
            if sentenceLength >= 3: # check sentence is long enough for inclusive/exclusive check
                if englishWords[sentencePointer] == "(3" and englishWords[sentencePointer + 1] == "incl)":
                    maoriWords.append("koutou")
                    sentencePointer += 2
                elif englishWords[sentencePointer] == "(2" and englishWords[sentencePointer + 1] == "incl)":
                    maoriWords.append("kōrua")
                    sentencePointer += 2
                elif englishWords[sentencePointer] == "(1" and englishWords[sentencePointer + 1] == "incl)":
                    maoriWords.append("koe")
                    sentencePointer += 2
            else:
                maoriWords.append("koe") # default is to assume singular inclusive you

        elif englishWords[sentencePointer] == "they":

            sentencePointer += 1
            if sentenceLength >= 3: # check sentence is long enough for inclusive/exclusive check
                if englishWords[sentencePointer] == "(3" and englishWords[sentencePointer + 1] == "excl)":
                    maoriWords.append("rātou")
                    sentencePointer += 2
                elif englishWords[sentencePointer] == "(2" and englishWords[sentencePointer + 1] == "excl)":
                    maoriWords.append("rāua")
                    sentencePointer += 2
            else:
                maoriWords.append("rāua")  # default is to assume two exclusive they

        elif englishWords[sentencePointer] == "we":

            sentencePointer += 1
            if sentenceLength >= 3:  # check sentence is long enough for inclusive/exclusive check
                if englishWords[sentencePointer] == "(3":

                    sentencePointer += 1
                    if englishWords[sentencePointer] == "excl)":
                        maoriWords.append("mātou")
                        sentencePointer += 1
                    elif englishWords[sentencePointer] == "incl)":
                        maoriWords.append("tātou")
                        sentencePointer += 1
                    else:
                        return INVALID

                if englishWords[sentencePointer] == "(2":

                    sentencePointer += 1
                    if englishWords[sentencePointer] == "excl)":
                        maoriWords.append("māua")
                        sentencePointer += 1
                    elif englishWords[sentencePointer] == "incl)":
                        maoriWords.append("tāua")
                        sentencePointer += 1
                    else:
                        return INVALID

            else:
                maoriWords.append("māua")  # default is to assume two exclusive we

        else:
            return INVALID

        if sentencePointer + 2 == sentenceLength: # check if list long enough for auxiliary verbs 'will' or 'am' and verb

            if englishWords[sentencePointer] == "am" or englishWords[sentencePointer] == "are":
                maoriWords.insert(0, getVerbPresent(englishWords[sentencePointer + 1]))

                if "invalid verb" in maoriWords[0]:  # if verb was invalid return message and end early
                    return maoriWords[0]
                else:
                    return ' '.join(maoriWords)

            elif englishWords[sentencePointer] == "will":
                maoriWords.insert(0, getVerbFuture(englishWords[sentencePointer + 1]))

                if "invalid verb" in maoriWords[0]:  # if verb was invalid return message and end early
                    return maoriWords[0]
                else:
                    return ' '.join(maoriWords)

            else:
                return INVALID

        elif sentencePointer + 1 == sentenceLength: # check if list long enough for verb
            maoriWords.insert(0, getVerbPastOrPresent(englishWords[sentencePointer]))

            if "invalid verb" in maoriWords[0]:  # if verb was invalid return message and end early
                return maoriWords[0]
            else:
                return ' '.join(maoriWords)


        else:
            return INVALID

    else:
        return INVALID


# read lines from stdin one at a time
for line in sys.stdin:
     print(translate(line))

# print(translate("We (2 excl) are going"))