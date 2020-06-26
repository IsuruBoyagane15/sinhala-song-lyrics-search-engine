import json


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

        # Fill the fields that are not found in original data with "Unknown"

        if "Lyrics" not in json_data:
            json_data['Lyrics'] = "Unknown"

        if "Music" not in json_data:
            json_data['Music'] = "Unknown"

        if "Genre" not in json_data:
            json_data['Genre'] = "Unknown"

        title = json_data["title"]
        if "–" in title:
            sep = "–"
        if "|" in title:
            sep = "|"
        if "-" in title:
            sep = "-"

        title_list = title.split(sep)
        title_en = title_list[0].strip()
        title_si = title_list[1].strip()

        json_data['title_en'] = title_en
        json_data['title_si'] = title_si
        json_data.pop('title')

        print(title_si,title_en)

        with open('processed/' + str(i) + '.json', 'w') as f:
            json.dump(json_data, f)


if __name__ == "__main__":
    process()
