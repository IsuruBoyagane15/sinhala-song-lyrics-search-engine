import json
import googletrans
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
            json_data = json.load(json_file)

        # Rename field named Tags to Genre
        if "Tags" in json_data:
            json_data['Genre'] = json_data["Tags"]
            json_data.pop('Tags')

        # Fill the fields that are not found in original data with "නොදනී"
        json_data = fill_missing(json_data)

        # Separate Sinhala title from title
        json_data = separate_title(json_data)

        # translate relevant fields to Sinhala
        json_data = translate(json_data)

        # convert numbers to int
        json_data['number_of_visits'] = int(json_data['number_of_visits'].replace(',', ''))
        json_data['number_of_shares'] = int(json_data['number_of_shares'])

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
            # A fix for unicode error
            # for k in translated:
            #     if k == 'චිත්\u200dරපට ගීත':
            #         translated.remove(k)
            #         translated.append("චිත්‍රපට ගීත")
        else:
            translated = translator.translate(song[i], dest='sinhala').text
        song[i] = translated
        print(song[i])
    print("================")
    return song


if __name__ == "__main__":
    process()