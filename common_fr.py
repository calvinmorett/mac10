from bs4 import BeautifulSoup
import requests
import re

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

with open('common_fr.txt') as common, open('common_fr_clean.txt', 'w') as common_clean:
    cleantext = BeautifulSoup(common, 'lxml').decode('iso-8859-1')
    cleantext = BeautifulSoup(cleantext, 'lxml').text
    cleantext = cleantext.strip().replace('.', '')
    cleantext = re.sub("[\(\[].*?[\)\]]", "", cleantext)
    cleantext = re.sub(r'[^a-zA-Z0-9-_]', ' ', cleantext)
    cleantext = ''.join(c for c in cleantext if not c.isdigit())
    cleantext = cleantext.replace('  ', ' ')
    cleantext = cleantext.replace('  ', ' ')
    cleantext = cleantext.replace('  ', '')
    cleantext = cleantext.split()
    # print(cleantext)
    common_clean.write(str(cleantext))
