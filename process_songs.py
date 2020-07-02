import json
import re
from googletrans import Translator


# Fill missing valies by ""
def fill_missing(song):
    if "Lyrics" not in song or song["Lyrics"] == "නොදන්නා":
        song['Lyrics'] = ""

    if "Music" not in song or song["Music"] == "නොදන්නා":
        song['Music'] = ""

    if "Genre" not in song or song["Genre"] == "නොදන්නා":
        song['Genre'] = ""
    return song


# seperate title content to sonhala and english and extract sinhala title
def separate_title(song):
    title = song["title"]
    for i in title:
        if i == "–":
            sep = "–"
        if i == "|":
            sep = "|"
        if i == "-":
            sep = "-"

    title_list = title.split(sep)
    title_sinhala = title_list[-1].strip()

    song['title'] = title_sinhala
    print(song['title'])
    return song


# clean beat data
def clean_beat(song):
    beat = song["beat"]
    if type(beat) == type([]):
        song['beat'] = beat[0].strip().split(" ", 1)[1]
    elif beat == "N/A":
        song['beat'] = ""
    return song


# replace dots in people names by space
def remove_dots_in_names(song):
    names = ["Artist", "Music", "Lyrics"]
    for i in names:
        field = song[i]
        if type(field) == type([]):
            for j in range(len(field)):
                field[j] = field[j].replace(".", " ")
        else:
            field = field.replace(".", " ")
        song.update({i: field})
    return song


# clean lyrics corpus
def clean_lyrics(song):
    lyrics = song['song_lyrics']
    lines = lyrics.split("\n")
    final = []
    for i, line in enumerate(lines):
        line = line.strip()
        line = re.sub('[.!?\\-—]', '', line)
        if not line or line.isspace() or '\u200d' in line:
            pass
        else:
            final.append(line)
    song["song_lyrics"] = "\n".join(final)
    return song


# translate sinhala artist name, composer name, lyricist name and genre to sinhala
def translate(song):
    translator = Translator()
    fields_to_translate = ["Artist", "Music", "Lyrics", "Genre"]
    for i in fields_to_translate:
        if type(song[i]) == list:
            translated = []
            for j in song[i]:
                j = j.strip()
                translated.append(translator.translate(j, dest='sinhala').text)
        else:
            song[i] = song[i].strip()
            translated = translator.translate(song[i], dest='sinhala').text
        song[i] = translated
    return song


def process():
    for i in range(510):
        with open("songs/" + str(i) + ".json") as json_file:
            song = json.load(json_file)

        # Rename field named Tags to Genre
        if "Tags" in song:
            song['Genre'] = song["Tags"]
            song.pop('Tags')

        # Fill the fields that are not found in original data with "නොදනී"
        song = fill_missing(song)

        # replace dots in names by space
        song = remove_dots_in_names(song)

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

        # process guitar_key
        if type(song["guitar_key"]) == type([]):
            song["guitar_key"] = song["guitar_key"][-1]
        song["guitar_key"] = song["guitar_key"].strip().lower()

        # write processed data to processed/ directory
        with open('processed/' + str(i) + '.json', 'w') as f:
            json.dump(song, f)


if __name__ == "__main__":
    process()
