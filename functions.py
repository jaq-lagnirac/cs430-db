import random
import tkinter as tk
from tkinter import messagebox

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
error_displayed = False

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

def getOneRandomSong(songList):
  MININDEX = 0
  MAXINDEX = 1999
  
  allSongs = songList
  randomNum = random.randrange(MININDEX, MAXINDEX)

  return(allSongs[randomNum])

# For any errors that may show up in the Search Page
def showError(error_message="An error occurred!"):
    global error_displayed
    if not error_displayed:
        error_displayed = True
        messagebox.showerror("Error", error_message)
        error_displayed = False  


# Checks if answers are valid and creates the query
def filterValidQuery(input):
    CONVERTDECIMAL = 100
    SECONDTOMILISECOND = 1000
    error_message = "Invalid Inputs"
    genre = []
    holdQueryVar = []
    valid = True

    # Set default genres if none are provided
    if not input.get("genres"):
        genre = [
            "pop", "Folk/Acoustic", "jazz", "metal", "R&B", "blues",
            "World/Traditional", "country", "easy listening", "rock",
            "Dance/Electronic", "hip hop", "latin", "classical"
        ]
    else:
        genre = list(input["genres"])

    # Validation rules for each field
    validation_rules = [
        ("minYear", lambda x: isinstance(x, int) and x >= 0),
        ("minLength", lambda x: isinstance(x, int) and x >= 0),
        ("maxPopularity", lambda x: isinstance(x, int) and x >= 0),
        ("maxEnergy", lambda x: isinstance(x, int) and x >= 0),
        ("maxYear", lambda x: isinstance(x, int) and x > input["minYear"]),
        ("maxLength", lambda x: isinstance(x, int) and x > input["minLength"]),
        ("maxDanceability", lambda x: isinstance(x, int) and x >= 0),
        ("maxTempo", lambda x: isinstance(x, int) and x >= 0),
    ]

    # Validate input fields
    for key, rule in validation_rules:
        value = input.get(key)
        if rule(value):
            holdQueryVar.append(value)
        else:
            valid = False
            showError(f"{key}: {error_message}")
            break  

    queryFilters = {
        "genre": {"$in":genre},
        "year": {"$gt":holdQueryVar[0], "$lt":holdQueryVar[4]},
        "duration_ms": {"$gt":(holdQueryVar[1]*SECONDTOMILISECOND), "$lt":(holdQueryVar[5]*SECONDTOMILISECOND)},
        "popularity": {"$gt": holdQueryVar[2]},
        "energy": {"$gt":(holdQueryVar[3]/CONVERTDECIMAL)},
        "danceability": {"$lt": (holdQueryVar[6]/CONVERTDECIMAL)},
        "tempo": {"$lt":holdQueryVar[7]}
    }

    validAndSongs = (valid, queryFilters)
    print(queryFilters)
    return validAndSongs


#In the 
def valdititySongArtistSubmit(sSong, sArtist):
    query = {}
    if ((sSong == "") and (sArtist== "")) or (not(sSong == "") and not(sArtist== "")):
        messagebox.showwarning("Warning", "Please search one at a time. (Note: Case-insensitive)")
    else:
        if not (sSong == ""):
            query = {"song": {"$regex": sSong, "$options": "i"}}
        else:
            query = {"artist": {"$regex": sArtist, "$options": "i"}}
            
    return query

def checkQuizValid(checkvar, radioChosen):
    EMPTY = "0"
    EMPTYLENGTH = 0
    validCheckbox = False
    validRadio = True  
    validSlider = True
    # Check if at least one checkbox is selected (Question 1 or 2)
    for valcheck in checkvar:
        #print("This is for the checkboxes:",valcheck.get())  
        if valcheck.get() != EMPTY:
            validCheckbox = True
            break  

    if not validCheckbox:
        messagebox.showerror("Error", "You haven't answered at least Question 1 or Question 2.")

    # Check if all radio buttons are selected (Questions 3-11)
    for valradio in radioChosen:
        #print("This is for the radio buttons:",valradio.get())  
        if valradio.get() == EMPTY:
            messagebox.showerror("Error", "You haven't finished answering Questions 4-11.")
            validRadio = False
            break  

    if len(sliderYear) == EMPTYLENGTH:
        validSlider = False
        messagebox.showerror("Error", "You haven't finished answering Question 3.")
        
        
    # Return True only if all conditions are valid
    return validCheckbox and validRadio and validSlider