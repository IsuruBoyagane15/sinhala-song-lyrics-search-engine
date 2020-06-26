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


        with open('processed/' + str(i) + '.json', 'w') as f:
            json.dump(json_data, f)

if __name__ == "__main__":
    process()
