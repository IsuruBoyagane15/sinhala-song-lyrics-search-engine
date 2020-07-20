# Sinhala song lyrics search engine


## Usage

1. Start Elasticsearch
2. Create the index by running utils.py
3. Start search engine app by running app.py 

## Lyrics and metadata

Following 9 metadata with the song lyrics fo 510 songs are used to create the index in Elasticsearch.

1. Title
2. Artist
3. Genre
4. Lyrics
5. Music
6. Guitar key (In English)
7. Beat
8. Number of views
9. Number of shares

## Data
- Original data directory - songs/
- Processed data directory - processed/

## Main Usecases

* Search by title/ beat/ guitar key etc. 
    - මාගෙ මතකේ ඔබේ
    - 6/8 සින්දු
    - චිත්‍රපට ගීත
* Search lyrics
    - වැසි වැටී වැව් ළිං 
* Multi Search 
    - ෂෙල්ටන් පෙරේරා තනුව කල ගීත
    - ක්ලැරන්ස් විජේවර්ධන ගායනා කල පැරණි පොප් සින්දු
* Sorted Range Queries 
    - ජනප්‍රියම සින්දු
    - ජනප්‍රියම 6/8 සින්දු 5
    - එඩ්වඩ් ජයකොඩි ගායනා කල ජනප්‍රියම සින්දු 5
* Filtering search results based on keywords (faceted search)

## Indexing techniques

Elasticsearch analysers are used in indexing.

## Qurying Procedure

![Alt text](querying_procedure.png?raw=true "Title")
