import json
import re
from googletrans import Translator


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

        # translate relevant fields to Sinhala
        song = translate(song)

        # convert numbers to int
        song['number_of_visits'] = int(song['number_of_visits'].replace(',', ''))
        song['number_of_shares'] = int(song['number_of_shares'])

        # clean song lyrics
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
        print(song["song_lyrics"])

        # with open('processed/' + str(i) + '.json', 'w') as f:
        #     json.dump(json_data, f)


def translate(song):
    translator = Translator()
    fields_to_translate = ["Artist", "Music", "Lyrics", "Genre"]
    for i in fields_to_translate:
        if type(song[i]) == list:
            # print(song[i])
            translated = []
            for j in song[i]:
                translated.append(translator.translate(j, dest='sinhala').text)
        else:
            translated = translator.translate(song[i], dest='sinhala').text
        song[i] = translated
        print(song[i])
    print("================")
    return song


if __name__ == "__main__":
    process()
