import time
import json
import re
from googletrans import Translator


# import mtranslate


def fill_missing(song):
    if "Lyrics" not in song:
        song['Lyrics'] = "නොදනී"

    if "Music" not in song:
        song['Music'] = "නොදනී"

    if "Genre" not in song:
        song['Genre'] = "නොදනී"
    return song


def separate_title(song):
    title = song["title"]
    if "–" in title:
        sep = "–"
    if "|" in title:
        sep = "|"
    if "-" in title:
        sep = "-"

    title_list = title.split(sep)
    title_sinhala = title_list[1].strip()

    song['title'] = title_sinhala
    return song


def clean_beat(song):
    beat = song["beat"]
    if type(beat) == type([]):
        song['beat'] = beat[0].strip().split(" ", 1)[1]
    elif beat == "N/A":
        song['beat'] = "නොදනී"
    return song


def clean_lyrics(song):
    lyrics = song['song_lyrics']
    lines = lyrics.split("\n")
    final = []
    for i, line in enumerate(lines):
        line = line.strip()
        line = re.sub('[.!?\\-—]', '', line)
        if not line or line.isspace() or '\u200d' in line:
            # if not line or line.isspace() or (line.isspace() and '\u200d' in line):
            pass
        else:
            final.append(line)
    song["song_lyrics"] = "\n".join(final)
    return song


def process():
    # fields = ["title", "Artist", 'Genre', 'Lyrics', 'Music', 'guitar_key', 'beat', 'song_lyrics', 'number_of_visits',
    #           'number_of_shares']

    for i in range(510):
        with open("songs/" + str(i) + ".json") as json_file:
            song = json.load(json_file)

        # Rename field named Tags to Genre
        if "Tags" in song:
            song['Genre'] = song["Tags"]
            song.pop('Tags')

        # Fill the fields that are not found in original data with "නොදනී"
        song = fill_missing(song)

        # Separate Sinhala title from title
        song = separate_title(song)

        # clean beat field
        song = clean_beat(song)

        # translate relevant fields to Sinhala
        song = translate(song)

        # convert numbers to int
        song['number_of_visits'] = int(song['number_of_visits'].replace(',', ''))
        song['number_of_shares'] = int(song['number_of_shares'])

        # clean song lyrics
        song = clean_lyrics(song)

        print(song)
        time.sleep(10)

        with open('processed/' + str(i) + '.json', 'w') as f:
            json.dump(song, f)


def translate(song):
    translator = Translator()
    fields_to_translate = ["Artist", "Music", "Lyrics", "Genre"]
    for i in fields_to_translate:
        if type(song[i]) == list:
            # print(song[i])
            translated = []
            for j in song[i]:
                j = j.strip()
                translated.append(translator.translate(j, dest='sinhala').text)
                # translated.append(mtranslate.translate(j, 'si', 'en'))
        else:
            song[i] = song[i].strip()
            translated = translator.translate(song[i], dest='sinhala').text
            # translated = mtranslate.translate(song[i], 'si', 'en')
        song[i] = translated
    print("================")
    return song


if __name__ == "__main__":
    process()
