from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re, itertools
from urllib.parse import urljoin
from collections import Counter, OrderedDict
import string

today = datetime.today()
week_num = today.strftime("%U")
myt = str(datetime.now().strftime('%m-%d-%Y'))

# ############
# idea:
# -[top.py] of the top10 charting songs, collect the artists + artists top 10 song
# -[getpage.py] extract and analyze top10 lyrics:
#   -[common.py, common_fr.py, getpage.py] remove common bridge-words; and, the, to, of, etc.
#   -[getpage.py] per song run frequency count of words
#     -[] if a word has a high frequency count, its font-size will be increased
#     -[] link every word back to song pages
#   -[] compare each artists top 10 song word-freq to each other and see any commonalities/patterns
# ############

with open('genius_top10_week'+str(week_num)+'_urls__'+myt+'.txt', 'r') as url_list:
    url_pass = url_list.read().splitlines()
    url_pass = list(url_pass)
    # list(url_pass)[index_counter])

url_list = open('genius_top10_week'+str(week_num)+'_urls__'+myt+'.txt', 'r')
print('\n'+'File opened: ', url_list,'\n')

def special_convert(varr):
    # The most common accents are the acute (é), grave (è), circumflex (â, î or ô), tilde (ñ),
    # umlaut and dieresis (ü or ï – the same symbol is used for two different purposes), and cedilla (ç).
    # Accent marks (also referred to as diacritics or diacriticals) usually appear above a character.
    # One exception is the cedilla, which appears directly underneath the letter c;
    # several less common accent marks appear next to the character.

    varr = varr
    varr = [x.replace('é', 'e') for x in varr] # acute (é)
    varr = [x.replace('è', 'e') for x in varr] # grave (è)
    varr = [x.replace('ê', 'e') for x in varr]
    varr = [x.replace('ç', 'c') for x in varr] # cedilla (ç)
    varr = [x.replace('à', 'a') for x in varr]
    varr = [x.replace('á', 'a') for x in varr]
    varr = [x.replace('ñ', 'n') for x in varr] # tilde (ñ),
    varr = [x.replace('ú', 'u') for x in varr]
    varr = [x.replace('ü', 'u') for x in varr] # umlaut and dieresis (ü or ï)
    varr = [x.replace('ï', 'u') for x in varr] # umlaut and dieresis (ü or ï)
    varr = [x.replace('í', 'i') for x in varr] # circumflex (â, î or ô)
    varr = [x.replace('â', 'a') for x in varr] # circumflex (â, î or ô)
    varr = [x.replace('ô', 'o') for x in varr] # circumflex (â, î or ô)
    return varr


def sort_lyrics(url_pass):
    r = requests.get(url_pass)
    encoding = r.encoding if "charset" in r.headers.get("content-type", "").lower() else None
    soup = BeautifulSoup(r.content, 'html.parser', from_encoding=encoding)
    # soup = BeautifulSoup(r.content, 'lxml', from_encoding=encoding)

    # Snag Page Title
    title = soup.title.string
    title = title.strip()
    title = title.replace(' | Genius Lyrics','')
    title = re.sub(r'[^a-zA-Z0-9-_]', '_', title)
    title = title.replace('__','_')
    title = title.replace('_Lyrics',' ')
    title = title.replace('__',' - ')
    title = title.replace('_',' ')
    title = title.strip()

    print('\n' + title + '\n' + url_pass)
    with open('genius_top10_week'+str(week_num)+'_lyrics__'+myt+'.txt', 'a+') as top10_analysis_export:
        top10_analysis_export.write('\n\n')
        top10_analysis_export.writelines(title)
        top10_analysis_export.write('\n')
        top10_analysis_export.writelines(url_pass)
        top10_analysis_export.write('\n')

    class_lyrics = soup.find("div", attrs={"class": "lyrics"}).text
    class_lyrics = class_lyrics.strip(string.punctuation)
    # print(class_lyrics) # prints all lyrics
    # class_lyrics = re.sub("[\(\[].*?[\)\]]", "", class_lyrics)
    class_lyrics = re.sub(r"\[.*\]","", class_lyrics)
    class_lyrics = class_lyrics.split()
    class_lyrics = [x.lower() for x in class_lyrics]
    class_lyrics = [x.strip(string.punctuation) for x in class_lyrics]
    class_lyrics = special_convert(class_lyrics)

    ######### lyrics
    common_words = [str(string.ascii_lowercase) , 'the', 'at', 'there', 'my', 'The', 'of', 'be', 'las', 'her', 'than', 'pa', 'this', 'an', 'a', 'to', 'from', 'which', 'like', 'been', 'in', 'or', 'she', 'him', 'is', 'do', 'into', 'who', 'you', 'had', 'how', 'oil', 'that', 'by', 'their', 'has', 'its', "c'que", 'it', 'word', 'if', 'look', 'now', 'he', 'but', 'will', 'two', 'find', 'was', 'not', 'up', 'more', 'long', 'for', 'what', 'other', 'write', 'down', 'on', 'all', 'about', 'go', 'day', 'are', 'were', 'out', 'They', 'did', 'as', 'we', 'many', 'cuando', 'get', 'with', 'when', 'then', 'no', 'come', 'his', 'your', 'them', 'way', "let's", 'they', 'can', 'these', 'tu', 'may', 'I', 'said', 'so', 'part', '', 'oh', 'le',  'him', 'her', 'it', 'them', 'de', 'any', 'of', 'from', 'un', 'a', 'an', 'one',  'at', 'in', 'tre', 'be', 'being', 'et', 'and', 'en', 'in', 'by', 'avoir', 'to', 'have', 'Non', 'que', 't', 'hat', 'which', 'en', 'who', 'whom', 'pour', 'for', 'in', 'order', 'to', 'dans', 'in', 'into', 'from', 'ce', 'this', 'that', 'il', 'he', 'it', 'qui', 'who', 'whom', 'ne', 'not', 'sur', 'on', 'upon', 'sour', 'se', 'pas', 'not', 'yeah', 'va', 'more', 'no', '?', 'pouvoir','be', 'able', 'la', 'c', 'ca', 'an', 'uh', 'par', 'by', 'je', 'I', 'avec', 'with', 'tout', 'all', 'very', 'faire', 'to', 'do', 'make', 'son', 'his', 'her', 'its', 'les', 'bran', 'mettre', 'put', 'place', 'autre', 'other', 'on', 'one', 'we', 'mais', 'but', 'nous', 'got', "i'd", 'we', 'us', 'comme', 've', 'as', 'ou', 'or', 'si', 'if', 'nigga', 'tu', 'leur', 'their', 'theirs', 'them', 'y', 'there', 'it', "you're", 'say', 'Those', 'elle', 'she', 'her', 'devoir', 'to', 'have', 'to', 'ow', 'e', 'Y', 'avant', 'mi', 'el', 'deux', 'two', 'm', 'me', "i'm", 'even', 'take', 'also', 'as', 'celui', 'that', 'the', 'one', 'he', 'him', 'donner', 'to', 'give', 'bien', "I'm", 'good', 'o', 'where', 'fois', 'vous', 'you', 'cest', 'che', 'yet', 'nouveau', 'new', 'new', 'aller', 'go', 'cela', 'that', 'it', 'entre', 'con', 'yo', 'vouloir', 'to', 'want', 'will', 'ere', 'd', 'j', 'muy', 'big', 'tall', 'mon', 'my', 'myself', 'moins', 'those', 'im', "est", "j'suis", 'aucun', 'none', 'te', "pa'", 'not', 'e', 'lui', 'lo', 'her', 'temps', 'tr', 's', 'very', 'savoir', 'to', 'Im', 'falloir', 'des', 'require', 'need', 'voir', 'see', 'vea', 'quelque', 'some', 'sans', 'ha', 'raison', 'moi', 'We', 'notre', 'our', 'dont', 'whose', 'of', 'which', 'non', 'no', 'not', 'an', "na'", 'monde', 'jour', 'day', 'i', 'to', 'ask', 'for', 'alors', 'then', 'so', 'apr', 's', 'na', 'trouver', 'to', 'ya', 'dernier', 'last', 'venir', 'to', 'tue', 'for', 'fossi', 'passer', 'to', 'too', 'peu', 'lequel', 'who', "c'est", 'whom', 'which', 'di', "j'ai", 'bon', 'good', 'depuis', 'at', 'ainsi', 'Mi','thus']

    new_lyric_list = comma_removal = [x.replace(',','') for x in class_lyrics]
    # para_removal = [x.replace("'",'') for x in comma_removal]
    # new_lyric_list = [html.escape(x) for x in comma_removal]

    # print(new_lyric_list)

    def CountFrequency(arr):
        return collections.Counter(arr)

    # Given a list of words, remove any that are
    # in a list of common words.
    def extract_common(list____keep, list____remove):
        x = [w for w in list____keep if w not in list____remove]
        # print(x)
        return x

    most_common_lyrics  = Counter(extract_common(new_lyric_list, common_words)).most_common(10)

    try:
        print(most_common_lyrics)
        with open('genius_top10_week'+str(week_num)+'_lyrics__'+myt+'.txt', 'a+') as top10_analysis_export:
            top10_analysis_export.write(str(most_common_lyrics))
            print('OK: Added New Entry!')
    except UnicodeEncodeError:
        pass
        with open('genius_top10_week'+str(week_num)+'_lyrics__'+myt+'.txt', 'a+') as top10_analysis_export:
            top10_analysis_export.write('Encoding Issue... No Lyrics Analyzed... Sorry Russians...')
            print('Issue: No New Entry... ')

index_counter = 0

def collect_analyze():
    global index_counter
    while url_list is not None:
        if index_counter == 0:
            topten_url = str(list(url_pass)[index_counter])
            sort_lyrics(topten_url)
            index_counter += 1
        else:
            topten_url = str(list(url_pass)[index_counter])
            sort_lyrics(topten_url)
            index_counter += 1

try:
    collect_analyze()
except IndexError:
    pass
    print('\n\nChecked top10!\n\n')
