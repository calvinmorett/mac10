from bs4 import BeautifulSoup
import requests
from datetime import *
import re
from urllib.parse import urljoin


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

###################
# ex, for testing #
base = "https://genius.com"
url = "https://genius.com/#top-songs"
###################

r = requests.get(url).text.encode('utf8').decode('ascii', 'ignore')
soup = BeautifulSoup(r, 'html.parser')

# Snag Page Title
title = soup.title.string
print('Page Title: ' + '\n' + title + '\n' + url + '\n')

top10 = soup.find("div", attrs={"id": "top-songs"})
top10_data = top10.findAll("a",href=True)

top10_song_url_list = []

for line in top10_data:
    if line:
        top10_song_heading3 = line.find("h3", attrs={"": ""})
        top10_song_heading3 = top10_song_heading3.text.strip().replace('Lyrics','   ')

        top10_artist_heading4 = line.find("h4", attrs={"": ""})
        top10_artist_heading4 = top10_artist_heading4.text.strip()

        if line['href']:
            relative = line['href']
            top10_song_url = urljoin(base, relative)
            print(top10_artist_heading4 + ' - ' + top10_song_heading3, top10_song_url, '\n')
            top10_song_url_list.append(top10_song_url)

    if len(top10_song_url_list) == 10:
        print('List of Top 10 URLS: ', top10_song_url_list)
        with open('genius_top10_week'+str(week_num)+'_urls__'+myt+'.txt', 'w+') as top10_takeout:
            print('File created ', top10_takeout)
            #top10_takeout.write(str(top10_song_url_list))
            for item in top10_song_url_list:
                top10_takeout.write("%s\n" % item)
