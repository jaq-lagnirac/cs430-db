import tkinter as tk 

answerToGenre = {
    "Dragon": "pop",
    "Unicorn": "Folk/Acoustic",
    "Mermaid": "jazz",
    "Fairy": "metal",
    "Goblin": "R&B",
    "Troll": "blues",
    "Phoenix": "World/Traditional",
    "Dinosaur age": "country",
    "Ancient Egypt": "easy listening",
    "Medieval Europe": "rock",
    "Future dystopia": "Dance/Electronic",
    "Pirate era": "hip hop",
    "Space exploration": "latin",
    "Fantasy world": "classical"
}
genres = []
sliderYear = []
parseRadio = []


#Gets the checkbox answer and converts it into the desired genre.
def addGenreQuery(checkBoxStatus):
    for checkbox in checkBoxStatus:
        if checkbox.get() in answerToGenre:
            genreValue = answerToGenre[checkbox.get()]
            genres.append(genreValue) 
    #print(genres)

#Converts given slider year to corresponding range
def updateYear(slide):
    yearRangeBottom = [1998,2009]
    yearRangeTop = [2010,2020]
    sliderYear.clear()
    if slide.get() <= 2009:
        sliderYear.append(yearRangeBottom)
    else:
        sliderYear.append(yearRangeTop)

#Gets the useable value from the radio buttons
def parseRadioValues(radioChosen):
    for val in radioChosen:
        storedVal = val.get()
        parseRadio.append(storedVal.split(","))
    

def makeQuery():
    try:
        query = {
            "genre": {"$in": genres},
            "year": {"$gt": int(sliderYear[0][0]),"$lt":int(sliderYear[0][1])},
            "duration_ms" : {"$gt": int(parseRadio[0][0]),"$lt":int(parseRadio[0][1])}, 
            "popularity": {"$gt": int(parseRadio[1][0]),"$lt":int(parseRadio[1][1])},
            "danceability": {"$gt": float(parseRadio[2][0]),"$lt":float(parseRadio[2][1])},
            "energy": {"$gt": float(parseRadio[3][0]),"$lt":float(parseRadio[3][1])},
            #"loudness": {"$gt": float(parseRadio[4][0]),"$lt":float(parseRadio[4][1])},  Decided not to use. Messes up querying.
            "speechiness": {"$gt": float(parseRadio[5][0]),"$lt":float(parseRadio[5][1])},
            "valence": {"$gt": float(parseRadio[6][0]),"$lt":float(parseRadio[6][1])},
            "tempo": {"$gt": int(parseRadio[7][0]),"$lt":int(parseRadio[7][1])}
        }
    except Exception as e:
        print(e)
        print("The user needs to answer all the radio buttons!")
    return query




