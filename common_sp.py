from bs4 import BeautifulSoup

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

# french
url = 'https://www.rypeapp.com/most-common-french-words/'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

class_lyrics = soup.find("div", attrs={"class": "lyrics"}).text
class_lyrics = re.sub("[\(\[].*?[\)\]]", "", class_lyrics)
# print(class_lyrics) # prints all lyrics
class_lyrics = class_lyrics.split()

with open('common.txt') as common, open('common_clean.txt', 'w') as common_clean:
    cleantext = BeautifulSoup(common, "lxml").text
    cleantext = ''.join(c for c in cleantext if not c.isdigit()).replace('.', '')
    ct = cleantext.strip()
    ct = ct.split()
    common_clean.write(str(ct))



div class wpb_text_column
find all b{bold}
