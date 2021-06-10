# ----------------------------------------------------- Imports --------------------------------------------------------
import glob
import json
import pickle
import re
from re import search
from string import punctuation
import emojis
import jsonlines
from nltk.corpus import stopwords
from string import digits


#------------------------------------------------------ Methonds -------------------------------------------------------


#-------------------------------------------------- Global Variables ---------------------------------------------------

# All files that we need
Global_Files = glob.glob("data\*.jl")

# saving Tweets from a party
party_dic = {}
party_tweets = {}
party_hashtags = {}
party_emoji = {}
german_stop_words_to_use =  ['aber', 'alle', 'allem', 'allen', 'aller', 'alles', 'als', 'also', 'am', 'an', 'ander', 'andere', 'anderem',
     'anderen', 'anderer', 'anderes', 'anderm', 'andern', 'anderr', 'anders', 'auch', 'auf', 'aus', 'bei', 'bin', 'bis',
     'bist', 'da', 'damit', 'dann', 'der', 'den', 'des', 'dem', 'die', 'das', 'dass', 'dass', 'derselbe', 'derselben',
     'denselben', 'desselben', 'demselben', 'dieselbe', 'dieselben', 'dasselbe', 'dazu', 'dein', 'deine', 'deinem',
     'deinen', 'deiner', 'deines', 'denn', 'derer', 'dessen', 'dich', 'dir', 'du', 'dies', 'diese', 'diesem', 'diesen',
     'dieser', 'dieses', 'doch', 'dort', 'durch', 'ein', 'eine', 'einem', 'einen', 'einer', 'eines', 'einig', 'einige',
     'einigem', 'einigen', 'einiger', 'einiges', 'einmal', 'er', 'ihn', 'ihm', 'es', 'etwas', 'euer', 'eure', 'eurem',
     'euren', 'eurer', 'eures', 'fuer', 'gegen', 'gewesen', 'hab', 'habe', 'haben', 'hat', 'hatte', 'hatten', 'hier',
     'hin', 'hinter', 'ich', 'mich', 'mir', 'ihr', 'ihre', 'ihrem', 'ihren', 'ihrer', 'ihres', 'euch', 'im', 'in',
     'indem', 'ins', 'ist', 'jede', 'jedem', 'jeden', 'jeder', 'jedes', 'jene', 'jenem', 'jenen', 'jener', 'jenes',
     'jetzt', 'kann', 'kein', 'keine', 'keinem', 'keinen', 'keiner', 'keines', 'koennen', 'koennte', 'machen', 'man',
     'manche', 'manchem', 'manchen', 'mancher', 'manches', 'mein', 'meine', 'meinem', 'meinen', 'meiner', 'meines',
     'mit', 'muss', 'musste', 'nach', 'nicht', 'nichts', 'noch', 'nun', 'nur', 'ob', 'oder', 'ohne', 'sehr', 'sein',
     'seine', 'seinem', 'seinen', 'seiner', 'seines', 'selbst', 'sich', 'sie', 'ihnen', 'sind', 'so', 'solche',
     'solchem', 'solchen', 'solcher', 'solches', 'soll', 'sollte', 'sondern', 'sonst', 'ueber', 'um', 'und', 'uns',
     'unsere', 'unserem', 'unseren', 'unser', 'unseres', 'unter', 'viel', 'vom', 'von', 'vor', 'waehrend', 'war',
     'waren', 'warst', 'was', 'weg', 'weil', 'weiter', 'welche', 'welchem', 'welchen', 'welcher', 'welches', 'wenn',
     'werde', 'werden', 'wie', 'wieder', 'will', 'wir', 'wird', 'wirst', 'wo', 'wollen', 'wollte', 'wuerde', 'wuerden',
     'zu', 'zum', 'zur', 'zwar', 'zwischen']

# ----------------------------------------------------- Methonds -------------------------------------------------------
def readFiles():
    error = []
    counter = 0



    for file in Global_Files:
        with jsonlines.open(file) as f:
            for item in f:
                try:
                    if item['http_status'] == 200:
                        if item['response']['meta']['result_count'] <= 0:
                            continue
                        mod_Tweets(item)

                    else:
                        error.append(item)
                except Exception as e:

                    raise e

    # Data of Fraktionslos is useless for our research
    party_tweets.__delitem__('Fraktionslos')
    party_dic["Tweets"] =party_tweets


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------- Moduls ---------------------------------------------------------

# gather all tweets to right party
def mod_Tweets(item):
    tweets = []
    for i in range(item['response']['meta']['result_count']):
        text = item['response']['data'][i]['text']
        if search("RT@", text):
            continue
        if search("RT",text):
            continue
        emoji_list = [i for i in emojis.get(text)]
        for l in emoji_list:
            #print(l)
            text = str(text) + str(l)

        hashtag_list = []
        if 'entities' not in item['response']['data'][i]:
            hashtag_list = []
        elif 'hashtags' not in item['response']['data'][i]['entities']:
            hashtag_list = []
        else:
            hashtag_list.extend(
                [j['tag'] for j in item['response']['data'][i]['entities']['hashtags']])
            for x in hashtag_list:
                #print(x)
                text = str(text) + str(x)

        text = umlauts(text)
        text = ''.join(text)
        text = txt_cleaner(text)
        tweets.append(text)

    if item['account_data']['Partei'] not in party_tweets:
        party_tweets[item['account_data']['Partei']] = tweets
    else:
        party_tweets[item['account_data']['Partei']].extend(tweets)


def umlauts(text):
    """
    Replace umlauts for a given text

    :param word: text as string--
    :return: manipulated text as str
    """
    new_text = []
    for word in text:
        #print(word)
        tempVar = word  # local variable

    # Using str.replace()

        tempVar = tempVar.replace('ä', 'ae')
        tempVar = tempVar.replace('ö', 'oe')
        tempVar = tempVar.replace('ü', 'ue')
        tempVar = tempVar.replace('Ä', 'Ae')
        tempVar = tempVar.replace('Ö', 'Oe')
        tempVar = tempVar.replace('Ü', 'Ue')
        tempVar = tempVar.replace('ß', 'ss')
        new_text.append(tempVar)


    return new_text

def txt_cleaner(text):
    new_text = str(text)
    new_text = new_text.lower()

    #remove punctuation
    remove_pun = str.maketrans('', '', punctuation)
    new_text = new_text.translate(remove_pun)
    #remove digits
    remove_digits = str.maketrans('', '', digits)
    new_text = new_text.translate(remove_digits)
    #stopwords
    new_text = [word for word in new_text.split() if word not in german_stop_words_to_use]
    new_text = ' '.join(new_text)
    new_text = ' '.join((new_text.strip('\n').split()))
    #remove http
    new_text = re.sub('(?:\s)http[^, ]*', '', new_text)
    return new_text

def to_Binary():
    #encoded_dict = str(party_dic).encode('utf-8')
    filehandler = open("output/tweets.pkl", 'wb')
    pickle.dump(party_dic, filehandler)

def emojiiFinder_light(text,item):
    emoji_list = [i for i in emojis.get(text)]

    if item['account_data']['Partei'] not in party_emoji:
        party_emoji[item['account_data']['Partei']] = emoji_list
    else:
        party_emoji[item['account_data']['Partei']].extend(emoji_list)

def to_json():
  jo = json.dumps(party_dic, indent=4)
  with open("output/TwitterData.json","w") as f:
      f.write(jo)


#----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------- Main -----------------------------------------------------------
readFiles()
to_json()

# -----------------------------------------------------------------------------------------------------------------------
