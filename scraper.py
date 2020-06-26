from bs4 import BeautifulSoup
import requests, time, os
import json, re
from lxml import etree
import pandas as pd

def process_content(key_val_pair):
    if key_val_pair:
        key_val_pair = key_val_pair.get_text()
        split_pair = key_val_pair.split(':')
        if len(split_pair) > 1:
            key = split_pair[0]
            val = split_pair[1]
            if ',' in val:
                values = []
                split_val = val.split(',')
                for value in split_val:
                    values.append(value)
                return key, values
            else:
                return key, val
        else:
            return None, None
    else:
        return None, None


def parse_lyrics(lyrics):
    space_set = set([' '])
    processed = ''
    regex = r"([A-z])+|[0-9]|\||-|∆|([.!?\\\/\(\)\+#&])+"
    lyric_lines = lyrics.split('\n')
    for line in lyric_lines:
        new = re.sub(regex, '', line)
        chars = set(new)
        if not ((chars == space_set) or (len(chars) is 0)):
            processed += new + '\n'
    return processed


def parse_html_song(html_pg):
    soup = BeautifulSoup(html_pg, 'html.parser')
    song = {}
    class_list = ["entry-tags", "entry-categories", "entry-author-name", "lyrics", "music"]
    title = soup.find('h1', {"class": "entry-title"}).get_text()
    print(title)
    # if "–" in title:
    #     sep = "–"
    # if "-" in title:
    #     sep = "-"
    # title_list = title.split(sep)
    # title_en = title_list[0].strip()
    # title_si = title_list[1].strip()

    # song.update({'title_en': title_en})
    # song.update({'title_si': title_si})
    song.update({'title': title})

    # print(title_en)
    # print(title_si)
    guit_key = soup.find_all('h3', {'class': None})[0].get_text().split('|')

    print(guit_key)
    if guit_key and len(guit_key) == 2:
        guitar_key = guit_key[0].split(':')
        if len(guitar_key) == 2:
            guitar_key = guitar_key[1].strip()
        beat = guit_key[1].split(':')
        if len(beat) == 2:
            beat = beat[1].strip()
    elif len(guit_key) == 1:
        guitar_key = guit_key[0].strip()
        beat = "N/A"
    else:
        guitar_key = "N/A"
        beat = "N/A"

    song.update({'guitar_key': guitar_key})
    song.update({'beat': beat})

    number_of_visits = soup.find('div', {'class': 'tptn_counter'}).get_text().split()[1].split('Visits')[0]
    song.update({'number_of_visits': number_of_visits})

    shares = soup.find('div', {'class': 'nc_tweetContainer swp_share_button total_shares total_sharesalt'}).get_text().split(" ")[0]
    song.update({'number_of_shares': shares})

    for class_l in class_list:
        content = soup.find_all('span', {"class": class_l})
        if content:
            key, val = process_content(content[0])
            if (not key is None) and (not val is None):
                song.update({key: val})
        else:
            pass
    unprocessed_lyrics = soup.select('pre')[0].get_text()
    processed_lyrics = parse_lyrics(unprocessed_lyrics)
    song.update({'song_lyrics': processed_lyrics})
    print(song)
    print("=======================================================")
    return song


def scrape_song_links():
    for page_number in range(5, 17):
        url = 'https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/?_page={}/'.format(page_number)
        print('Scraping the URL : ', url)

        headers = requests.utils.default_headers()
        response = requests.get(url, headers)
        page = response.text

        links = []
        soup = BeautifulSoup(page, 'html.parser')
        song_links = soup.find_all("a", {"class": "_blank"})
        for tag in song_links:
            link = tag.get('href')
            links.append(link)

        with open('song_links.csv', 'a') as f:
            for link in links:
                f.write(link + os.linesep)
        time.sleep(10)


def scrape_songs():
    next_song = 0
    while next_song < 510:
        print('Scraping song', next_song)

        with open('song_links.csv', 'r') as f:
            lines = f.readlines()
        url = lines[next_song]

        headers = requests.utils.default_headers()
        res = requests.get(url, headers)
        html_doc = res.text

        song = parse_html_song(html_doc)

        with open('songs/' + str(next_song) + '.json', 'w') as f:
            json.dump(song, f)
        next_song += 1

        time.sleep(20)


if __name__ == "__main__":
    # scrape_song_links()
    scrape_songs()
