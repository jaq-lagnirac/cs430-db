import tkinter as tk
from tkinter import messagebox
import math
import numpy as np
import functions as func
import mongodbConnect as mdb

error_displayed = func.error_displayed

def main():
    def showHomePage():
        home.pack(fill="both", expand=True)
        search.pack_forget()
        randomSong.pack_forget()
        playlist.pack_forget()
        quizResults.pack_forget()
        if quizFrames:
            for frame in quizFrames:
                frame.pack_forget()
        
        #From the Search Page, if home is click, reset the page.
        genre.set("Select a Genre")
        minYear.set(0)
        minLength.set(0)
        maxPopularity.set(0)
        maxEnergy.set(0)
        maxYear.set(0)
        maxLength.set(0)
        maxDanceability.set(0)
        maxTempo.set(0)
        searchSong.set(value="")
        searchArtist.set(value="")
        addGenreSearch.clear()

    def showQuiz():
        home.pack_forget()
        search.pack_forget()
        randomSong.pack_forget()
        playlist.pack_forget()
        quizResults.pack_forget()
        if quizFrames:
            quizFrames[0].pack(fill="both", expand=True)

    def showQuizResults():
        quizResults.pack(fill="both", expand=True)
        home.pack_forget()
        search.pack_forget()
        randomSong.pack_forget()
        playlist.pack_forget()
        if quizFrames:
            for frame in quizFrames:
                frame.pack_forget()

    def showSearch():
        search.pack(fill="both", expand=True)
        home.pack_forget()
        randomSong.pack_forget()
        playlist.pack_forget()
        quizResults.pack_forget()
        if quizFrames:
            for frame in quizFrames:
                frame.pack_forget()

    def showRandomSong():
        randomSong.pack(fill="both", expand=True)
        home.pack_forget()
        search.pack_forget()
        playlist.pack_forget()
        quizResults.pack_forget()
        if quizFrames:
            for frame in quizFrames:
                frame.pack_forget()

    def showPlaylist():
        playlist.pack(fill="both", expand=True)
        home.pack_forget()
        search.pack_forget()
        randomSong.pack_forget()
        quizResults.pack_forget()
        if quizFrames:
            for frame in quizFrames:
                frame.pack_forget()

    def selectOption(questionType):
        if questionType == "Radiobuttons":
            quizLabel.config(text="You selected: " + str(ans.get()))
        elif questionType == "Slider":
            quizLabel.config(text="You selected: " + str(ans.get()))

    def goNext(index):
        if index < len(quizFrames) - 1:
            #Hide current frame
            quizFrames[index].pack_forget()
            #Show next frame
            quizFrames[index + 1].pack(fill="both", expand=True)

    def goBack(index):
        if index > 0:
            #Hide current frame
            quizFrames[index].pack_forget()
            #Show previous frame
            quizFrames[index - 1].pack(fill="both", expand=True)


    #Checks if all the questions on the quiz have been answered
    #If so prints the query
    #!!!Need to Add Frame function to where all the songs show on gui!!!
    #!!!Need to add: When changing to song page, reset all the answers!!!
    def checkQuiz():
        valid = func.checkQuizValid(checkVar, radioChosenAnswers)
        #print(valid)
        if valid == True:
            #ADD HERE
            songs = printQuery()
            
            #Also go to display quiz page
            showQuizResults()
        else:
            print("There has been an error")
    
    #Function to check if the Querying works
    def printQuery():
        #Makes the user responses useable
        func.parseRadioValues(radioChosenAnswers)
        func.addGenreQuery(checkVar)
        #Handles the Querying
        query = func.makeQuery()
        mdb.printQuery(query)
        #This stores all the songs the query returns
        #This is a Mongodb cursor
        #Access by using for loop when needed and each song is a dictionary with the fields being the keys.
        #songs is already a list
        songs = mdb.find_all(query)
        #print(songs)
        print("----Works-----")
        return songs
    
    #Functions in the Search Frame   
    def addDropdownGenres():
        if genre.get() != "Select a Genre":
            addGenreSearch.add(genre.get())
        print(addGenreSearch)
    
    def deleteList():
        addGenreSearch.clear()
        print(addGenreSearch)
    

    #Submit button for Song options in Search:
    def submitSearchOptions():
        VALIDITYINDEX = 0
        QUERYRESULT = 1
        
        #Hold All Filter Choices
        try:
            # Safely construct the dictionary
            filterChoices = {
                "genres": addGenreSearch,  
                "minYear": minYear.get(),
                "minLength": minLength.get(),
                "maxPopularity": maxPopularity.get(),
                "maxEnergy": maxEnergy.get(),
                "maxYear": maxYear.get(),
                "maxLength": maxLength.get(),
                "maxDanceability": maxDanceability.get(),
                "maxTempo": maxTempo.get()
            }
            results = func.filterValidQuery(filterChoices)
            #Checks if Query is valid
            if(results[VALIDITYINDEX] == True):
                print("Query is valid")
                mdb.getSearchFilterQuery(results[QUERYRESULT])
            else:
                #Notify the user that something went wrong 
                print("Something went wrong")
                pass
        except Exception as e:
            print("An unexpected error occurred:", e)
            messagebox.showerror("Error","You entered a value this is not a number. OR You have not set a Max Year and Max Length")

        #print(filterChoices)

    def goSearch():
        #search for the songs based on input
        #replace this code with searching function:
        '''
        home.pack(fill="both", expand=True)
        search.pack_forget()
        randomSong.pack_forget()
        playlist.pack_forget()
        if quizFrames:
            for frame in quizFrames:
                frame.pack_forget()
        '''
        
        searchedSong = searchSong.get()
        searchedArtist = searchArtist.get()
        
        #print("Printing:",searchedSong,searchedArtist)
        querySongArtist = func.valdititySongArtistSubmit(searchedSong, searchedArtist)
        #print("Printing:",querySongArtist)
        if not querySongArtist:
            print("Something went wrong")
        else:
            mdb.getSearchFilterQuery(querySongArtist)
            print("It worked")

    #Instructions for the Search Page
    def showInstructions():
        INSTRUCTION = '''
        "minYear"-Input in a whole, non-negative number (Min Year: 2000)
        
        "minLength"-Input in a whole, non-negative number (seconds)
        
        "maxPopularity"- Input a whole, non-negative number (0-100)
        
        "maxEnergy"- Input a whole, non-negative number (0-100)
        
        "maxYear"- Input a whole, non-negative number that is greater than minYear (Max Year: 2020)
        
        "maxLength"- Input in a whole, non-negative number that is greater than minLength (seconds)
        
        "maxDanceability"- Input a whole, non-negative number (0-100)
        
        "maxTempo"- Input a whole, non-negative number (0-250)
        '''
        messagebox.showinfo("showinfo", INSTRUCTION)


    root = tk.Tk()
    root.title("Truify")
    #what size window do we need?
    root.geometry("800x700")

    #Frames for each page
    home = tk.Frame(root)
    search = tk.Frame(root)
    randomSong = tk.Frame(root)
    playlist = tk.Frame(root)
    quizResults = tk.Frame(root)

    #HOME PAGE COMPONENTS
    truifyLabel = tk.Label(home, text="Truify", font=("Lucida Sans", 24, "bold"))
    quizButton = tk.Button(home, text="Quiz", command=showQuiz, bg='black', fg='white', font=("Georgia", 18, "bold"), padx=10, pady=10)
    searchButton = tk.Button(home, text="Search", command=showSearch, bg='black', fg='white', font=("Georgia", 18, "bold"), padx=10, pady=10)
    randomButton = tk.Button(home, text="Random Song", command=showRandomSong, bg='black', fg='white', font=("Georgia", 18, "bold"), padx=10, pady=10)
    playlistButton = tk.Button(home, text="Playlist", command=showPlaylist, bg='black', fg='white', font=("Georgia", 18, "bold"), padx=10, pady=10)

    # Place in frames
    truifyLabel.pack(pady=20)
    quizButton.pack(pady=10)
    searchButton.pack(pady=10)
    randomButton.pack(pady=10)
    playlistButton.pack(pady=10)
    
    #QUIZ COMPONENTS
    # Questions List:
    # question, type of question, answers, category of attribute, attributes
    questions = [
        {
            "question": "Which of the following would you like to be real?\n(You can choose more than one)",
            "questionType": "Checkboxes",
            "answer": ["Dragon", "Unicorn", "Mermaid", "Fairy", "Goblin", "Troll", "Phoenix"],
            "category": "Genre",
            "attribute": ["pop", "Folk/Acoustic", "jazz", "metal", "R&B", "blues", "World/Traditional"]
        },
        {
            "question": "If you could time travel, where would you go?\n(You can choose more than one)",
            "questionType": "Checkboxes",
            "answer": ["Dinosaur age", "Ancient Egypt", "Medieval Europe", "Future dystopia", "Pirate era", "Space exploration", "Fantasy world"],
            "category": "Genre",
            "attribute": ["country", "Easy Listening", "rock", "Dance/Electronic", "hip hop", "latin", "classical"]
        },
        {
            "question": "What year would you like to revisit?",
            "questionType": "Slider",
            "answer":[1998,2020],
            "category": "Song Year Interval",
            "attribute": ["1998,2011","2008,2020"]
        }, 
        {
            "question": "Which party game would you rather play?",
            "questionType": "Radiobuttons",
            "answer": ["Monopoly", "Uno", "Charades", "Pictionary"],
            "category": "Song Length",
            "attribute": ["113000,384000", "120000,350000", "100000,384000", "200000,485000"] # measured in ms
        },
        {
            "question": "Which emoji are you?",
            "questionType": "Radiobuttons",
            "answer": ["😂", "💀", "😑", "😏"],
            "category": "Popularity",
            "attribute": ["20,100", "0,60", "25,75", "5,77"]
        },
        {
            "question": "Would you rather not have hands or feet?",
            "questionType": "Radiobuttons",
            "answer": ["Hands", "Feet"],
            "category": "Danceability",
            "attribute": ["0.3,1", "0,0.80"]
        },
        {
            "question": "What's your go to drink?",
            "questionType": "Radiobuttons",
            "answer": ["Coffee", "Tea", "Water", "Energy Drinks", "Alcohol"],
            "category": "Energy",
            "attribute": ["0.25,1", "0.1,0.8", "0.2,1", "0.3,1", "0,0.5"]
        },
        {
            "question": "Out of these options, which one would you choose\nto wake you up for the rest of your life?\n(They could happen at any time)",
            "questionType": "Radiobuttons",
            "answer": ["Standard alarm sound", "Metal Pipe falling sound effect", "Fire Alarm"],
            "category": "Loudness",
            "attribute": ["-16,-0.1", "-0.14, -0.2", "-20.6,-3"] #DECIDED NOT USE FOR QUERY
        },
        {
            "question": "Imagine you are talking with someone, then you zone out.\nHow would you respond?",
            "questionType": "Radiobuttons",
            "answer": ["Huh", "What", "Can you say that again", "Respond with 'Yea' while nodding your head and pretend you heard them"],
            "category": "Speechness",
            "attribute": ["0.01,0.4", "0,0.5", "0.07,0.3", "0.03,0.6"]
        },
        {
            "question": "Are you happy?",
            "questionType": "Radiobuttons",
            "answer": ["Yes", "No"],
            "category": "Valence",
            "attribute": ["0.3,1", "0,0.8"]
        },
        {
            "question": "What would you rather be doing right now?",
            "questionType": "Radiobuttons",
            "answer": ["Sleeping", "Hanging out with Friends", "Watching your favorite show/movie", "Doing your hobby"],
            "category": "Tempo",
            "attribute": ["0,120", "80,211", "60,125", "80,170"]
        },
    ]

    #Create frames for each question
    quizFrames = []

    #Store the values for the checkboxes
    checkVar = []
    
    #Store the values for the radiobuttons
    radioChosenAnswers = []
    
    quizcounter = 0 
    FIRSTQUESTIONINDEX = 1
    LASTQUESTIONINDEX = 11

    #Setup for Quiz Questions 
    for question in questions:
        #Answer Default Value
        ans = tk.StringVar(value=None)
        vars = tk.StringVar(value=0)
        
        #Add frame
        quiz = tk.Frame(root)
        quizTitle = tk.Label(quiz, text="Quiz", font=("Georgia", 25, "bold"))
        quizTitle.pack(pady=5, padx=20)
        questionLabel = tk.Label(quiz, text=("Q" + str(questions.index(question) + 1) + ". " + question['question']), font=("Lucida Sans", 14), width = 60)
        questionLabel.pack(anchor='w', pady=20, padx=20)

        quizLabel = tk.Label(quiz, text="Please make a selection", font=("Lucida Sans", 12))
        counter = 0                
        
        #if radio button:
        if question['questionType'] == "Radiobuttons":
            for answer in question['answer']:
                #Puts the users answer into list
                if vars not in radioChosenAnswers:
                    radioChosenAnswers.append(vars)
                radio_button = tk.Radiobutton(
                    quiz, 
                    text=answer, 
                    font=("Lucida Sans", 12), 
                    variable=vars, 
                    value=question['attribute'][counter],
                    command=selectOption(question['questionType'][counter])
                )
                
                radio_button.pack(anchor='w', pady=5, padx=20)
                if counter < len(question['attribute']):
                    counter += 1

            # Submit Button for the Quiz
            if quizcounter == LASTQUESTIONINDEX - 1: 
                submitQuizButton = tk.Button(quiz, text="Submit", command=checkQuiz,  bg='red', fg='white', font=("Lucida Sans", 14), padx=5, pady=5)
                submitQuizButton.pack(side="right", padx=75, pady=5)
                
            quizcounter += 1
        elif question['questionType'] == "Checkboxes":
            for answer in question['answer']:
                var = tk.StringVar(value=0)
                #Stores the values of the user into list
                checkVar.append(var)
                checkbox = tk.Checkbutton(quiz, text=answer, font=("Lucida Sans", 12), variable=var, onvalue=answer, offvalue="Nothing", command=selectOption(question['questionType']))
                checkbox.pack(anchor='w', pady=5, padx=20)
            quizcounter += 1    
        elif question['questionType'] == "Slider":
            # sliderLabel = tk.Label(quiz, text="Slider questions not ready yet", font=("Lucida Sans", 12))
            # sliderLabel.pack(pady=10)
            sliderVar = tk.IntVar(value=None)
            slider = tk.Scale(quiz, variable=sliderVar, from_=(question['answer'][0]), to=(question['answer'][1]), orient="horizontal",)
            slider.pack(pady=5, padx=20)
            
            #Used to update the slider
            submitbutton = tk.Button(quiz, text="Submit the Year", command=lambda: func.updateYear(slider))
            submitbutton.pack()

            quizcounter += 1
        # Show answer
        # quizLabel.pack(pady=10)
        quizFrames.append(quiz)

        nextButton = tk.Button(quiz, text="Next", command=lambda index=len(quizFrames)-1: goNext(index), bg='black', fg='white', font=("Lucida Sans", 14), padx=5, pady=5)
        backButton = tk.Button(quiz, text="Back", command=lambda index=len(quizFrames)-1: goBack(index), bg='black', fg='white', font=("Lucida Sans", 14), padx=5, pady=5)

        nextButton.pack(side="right", padx=75, pady=5)
        backButton.pack(side="left", padx=75, pady=5)
        if quizcounter == LASTQUESTIONINDEX: 
            nextButton.pack_forget()
        elif quizcounter == FIRSTQUESTIONINDEX:
            backButton.pack_forget()
 
    addGenreSearch = set()



    #QUIZ RESULT COMPONENTS
    
    songSuggestions = [
        {
            "title": "a song",
            "artist": "an artist",
            "release_date": "a date",
            "genre": "a genre"
        },
        {
            "title": "another song",
            "artist": "another artist",
            "release_date": "another date",
            "genre": "another genre"
        },
        {
            "title": "third song",
            "artist": "third artist",
            "release_date": "third date",
            "genre": "third genre"
        },
        {
            "title": "fourth song",
            "artist": "fourth artist",
            "release_date": "fourth date",
            "genre": "fourth genre"
        },
        {
            "title": "fifth song",
            "artist": "an artist",
            "release_date": "a date",
            "genre": "a genre"
        },
        {
            "title": "sixth song",
            "artist": "another artist",
            "release_date": "another date",
            "genre": "another genre"
        },
        {
            "title": "seventh song",
            "artist": "third artist",
            "release_date": "third date",
            "genre": "third genre"
        },
        {
            "title": "eighth song",
            "artist": "fourth artist",
            "release_date": "fourth date",
            "genre": "fourth genre"
        },
    ]

    # starting index
    startIndex = 0

    def loadSongs(startIndex):
        # Clear the current frame content
        for frame in quizResults.winfo_children():
            frame.grid_forget()
        
        # Set the current row to start rendering songs
        quizTitleRow = 0
        quizTitleCol = 0
        currentRow = quizTitleRow + 1
        
        # Loop through and load the current set of songs
        for i in range(startIndex, min(startIndex + 4, len(songSuggestions))): 
            
            #Home button
            quizHomeButton = tk.Button(quizResults, text="Home", command=showHomePage, bg='white', fg='black', font=("Lucida Sans", 12))
            quizHomeButton.grid(sticky = "w", row = quizTitleRow, column = quizTitleCol, pady=20, padx=20)
            
            #Quiz results label
            quizResultsTitle = tk.Label(quizResults, text="Song Suggestions", font=("Georgia", 25, "bold"))
            quizResultsTitle.grid(row = quizTitleRow, column = quizTitleCol + 1, pady=5, padx=20, columnspan = 100)
            song = songSuggestions[i]
            column = (i % 2)

            songName = tk.Label(quizResults, text=f"{i + 1}. {song['title']}", font=("Lucida Sans", 14, "bold"))
            songName.grid(row=currentRow, column=column * 2, pady=(25, 10), padx=20)

            artistName = tk.Label(quizResults, text=f"Artist: {song['artist']}", font=("Lucida Sans", 12))
            artistName.grid(row=currentRow + 1, column=column * 2, pady=5, padx=20)

            releaseName = tk.Label(quizResults, text=f"Release Date: {song['release_date']}", font=("Lucida Sans", 12))
            releaseName.grid(row=currentRow + 2, column=column * 2, pady=5, padx=20)

            genreName = tk.Label(quizResults, text=f"Genre: {song['genre']}", font=("Lucida Sans", 12))
            genreName.grid(row=currentRow + 3, column=column * 2, pady=5, padx=20)

            addPlaylistButton = tk.Button(quizResults, text="Add to Playlist", bg='white', fg='black', font=("Lucida Sans", 12))
            addPlaylistButton.grid(row=currentRow + 4, column=column * 2, pady=20, padx=20)

            if column == 1:
                currentRow += 5

        # Add "Next" button
        if startIndex + 4 < len(songSuggestions):
            nextSongsbutton = tk.Button(quizResults, text="Next", command=lambda: loadNextFrame(startIndex, startIndex + 4), bg='black', fg='white', font=("Lucida Sans", 14))
            nextSongsbutton.grid(row=currentRow, column=1, pady=20, padx=20)

        # Add "Back" button
        if startIndex > 0:
            backSongsButton = tk.Button(quizResults, text="Back", command=lambda: loadNextFrame(startIndex, startIndex - 4), bg='black', fg='white', font=("Lucida Sans", 14))
            backSongsButton.grid(row=currentRow, column=0, pady=20, padx=20)

    def loadNextFrame(startIndex, newStartIndex):
        startIndex = newStartIndex
        loadSongs(startIndex)

    # Load first set of songs
    loadSongs(startIndex)

    #SEARCH COMPONENTS
    titleRow = 0
    titleCol = 0
    #Home button
    homeButton = tk.Button(search, text="Home", command=showHomePage, bg='white', fg='black', font=("Lucida Sans", 12))
    homeButton.grid(sticky = "w", row = titleRow, column = titleCol, pady=20, padx=20, columnspan = 100)

    #Instruction Button
    instructionButton = tk.Button(search, text="Instructions", bg='white', fg='black', font=("Lucida Sans", 12), command=showInstructions )
    instructionButton.grid(sticky = "e", row = titleRow, column = titleCol + 2, pady=20, padx=20, columnspan = 100)
    
    #Search label
    searchTitle = tk.Label(search, text="Search", font=("Georgia", 25, "bold"))
    searchTitle.grid(row = titleRow, column = titleCol, pady=5, padx=20, columnspan = 100)

    # which types are these?
    genreOptions = ["pop","Folk/Acoustic","jazz","metal",
                    "R&B","blues","World/Traditional","country",
                    "easy listening","rock","Dance/Electronic",
                    "hip hop","latin","classical"]  
    global genre
    genre = tk.StringVar()
    genre.set("Select a Genre")
    global minYear
    minYear = tk.IntVar()
    global minLength
    minLength = tk.IntVar()
    global maxPopularity
    maxPopularity = tk.IntVar()
    global maxEnergy
    maxEnergy = tk.IntVar()
    global maxYear
    maxYear = tk.IntVar()
    global maxLength
    maxLength = tk.IntVar()
    global maxDanceability
    maxDanceability = tk.IntVar()
    global maxTempo
    maxTempo = tk.IntVar()
    global searchSong
    searchSong = tk.StringVar()
    global searchArtist
    searchArtist = tk.StringVar()
    
    genreInput = tk.OptionMenu(search, genre, *genreOptions)
    genreInput.config(bg="black", fg="white", font=("Lucida Sans", 12))
    buttonAddGenreDropDown = tk.Button(search, text="Add Genre", command=addDropdownGenres)
    buttonAddGenreDropDown.config(bg="black", fg="white", font=("Lucida Sans", 12))
    buttonDeleteGenreList = tk.Button(search, text="Delete Genre List", command=deleteList)
    buttonDeleteGenreList.config(bg="black", fg="white", font=("Lucida Sans", 12))
    
    minYearLabel = tk.Label(search, text="Min year :", font=("Lucida Sans", 12))
    minYearInput = tk.Entry(search, textvariable=minYear, bg='black', fg='white')
    maxYearLabel = tk.Label(search, text="Max year:", font=("Lucida Sans", 12))
    maxYearInput = tk.Entry(search, textvariable=maxYear, bg='black', fg='white')
    
    minLengthLabel = tk.Label(search, text="Min Length:", font=("Lucida Sans", 12))
    minLengthInput = tk.Entry(search, textvariable=minLength, bg='black', fg='white')
    maxLengthLabel = tk.Label(search, text="Max Length:", font=("Lucida Sans", 12))
    maxLengthInput = tk.Entry(search, textvariable=maxLength, bg='black', fg='white')

    maxPopLabel = tk.Label(search, text="Min Popularity:", font=("Lucida Sans", 12))
    maxDanceLabel = tk.Label(search, text="Max Danceability:", font=("Lucida Sans", 12))
    maxEnergyLabel = tk.Label(search, text="Min Energy:", font=("Lucida Sans", 12))
    maxTempoLabel = tk.Label(search, text="Max Tempo:", font=("Lucida Sans", 12))

    maxPopularityInput = tk.Entry(search, textvariable=maxPopularity, bg='black', fg='white')
    maxEnergyInput = tk.Entry(search, textvariable=maxEnergy, bg='black', fg='white')
    maxLengthInput = tk.Entry(search, textvariable=maxLength, bg='black', fg='white')
    maxDanceabilityInput = tk.Entry(search, textvariable=maxDanceability, bg='black', fg='white')
    maxTempoInput = tk.Entry(search, textvariable=maxTempo, bg='black', fg='white')

    buttonSubmitOptions = tk.Button(search, text="Submit Filters", command=submitSearchOptions)
    buttonSubmitOptions.config(bg="black", fg="white", font=("Lucida Sans", 12))
    
    searchSongLabel = tk.Label(search, text="Search Song:", font=("Lucida Sans", 12))
    searchSongInput = tk.Entry(search, textvariable=searchSong, bg='black', fg='white')

    searchArtistLabel = tk.Label(search, text="Search Artist:", font=("Lucida Sans", 12))
    searchArtistInput = tk.Entry(search, textvariable=searchArtist, bg='black', fg='white')

    genreRow = titleRow + 1
    genreCol = titleCol
    genreInput.grid(row = genreRow, column = genreCol, columnspan = 100, padx = 15, pady = 25)
    buttonAddGenreDropDown.grid(row = genreRow, column =  genreCol + 2, columnspan= 50, padx = 15, pady= 25) #Dont know how to fix styling to match
    buttonDeleteGenreList.grid(row = genreRow, column =  genreCol + 4, columnspan= 50, padx = 15, pady= 25) #Dont know how to fix styling to match
    
    mYRow = genreRow + 1
    mYCol = genreCol
    minYearLabel.grid(sticky = "w", row= mYRow, column= mYCol, padx=15, pady = 10)
    minYearInput.grid(sticky = "w", row= mYRow, column= mYCol + 1)
    maxYearLabel.grid(sticky = "w", row= mYRow, column= mYCol + 2, padx=10)
    maxYearInput.grid(sticky = "w", row= mYRow, column= mYCol + 3)

    mLRow = mYRow + 1
    mLCol = mYCol
    minLengthLabel.grid(sticky = "w", row= mLRow, column= mLCol, padx=15, pady = 10)
    minLengthInput.grid(sticky = "w", row= mLRow, column= mLCol + 1)
    maxLengthLabel.grid(sticky = "w", row= mLRow, column= mLCol + 2, padx=10)
    maxLengthInput.grid(sticky = "w", row= mLRow, column= mLCol + 3)

    mPRow = mLRow + 1
    mPCol = mLCol
    maxPopLabel.grid(sticky = "w", row= mPRow, column= mPCol, padx=15, pady = 10)
    maxPopularityInput.grid(sticky = "w", row= mPRow, column= mPCol + 1)
    maxDanceLabel.grid(sticky = "w", row= mPRow, column= mPCol + 2, padx=10)
    maxDanceabilityInput.grid(sticky = "w", row= mPRow, column= mPCol + 3)

    mERow = mPRow + 1
    mECol = mPCol
    maxEnergyLabel.grid(sticky = "w", row= mERow, column= mECol, padx = 15, pady = (10, 30))
    maxEnergyInput.grid(sticky = "w", row= mERow, column= mECol + 1, pady = (10, 30))
    maxTempoLabel.grid(sticky = "w", row= mERow, column= mECol + 2, padx=10, pady = (10, 30))
    maxTempoInput.grid(sticky = "w", row= mERow, column= mECol + 3, pady = (10, 30))

    filterSubRow = mERow + 1
    filterSubCol = mECol
    buttonSubmitOptions.grid(sticky = "w", row= filterSubRow, column= filterSubCol + 1, pady = (10, 30))

    searchSongRow = filterSubRow + 1
    searchSongCol = filterSubCol
    searchSongLabel.grid(sticky = "w", row = searchSongRow, column= searchSongCol, padx = (15, 0))
    searchSongInput.grid(sticky = "NESW", row= searchSongRow, column= searchSongCol + 1, columnspan=100, pady = 15)

    searchArtistRow = searchSongRow + 1
    searchArtistCol = searchSongCol
    searchArtistLabel.grid(sticky = "w", row = searchArtistRow, column= searchArtistCol, padx = (15, 0))
    searchArtistInput.grid(sticky = "NESW", row = searchArtistRow, column= searchArtistCol + 1, columnspan=100, pady = 15)

    searchRow = searchArtistRow + 1
    searchCol = searchArtistCol

    searchButton = tk.Button(search, text="Search", command=goSearch, bg='white', fg='black', font=("Lucida Sans", 14), padx = 5, pady = 5)
    searchButton.grid(row = searchRow, column = searchCol, pady=20, padx=20, columnspan = 100)

    #RANDOM SONG COMPONENTS
    allSongs = mdb.getAllSongs()
    #Stores random song object to use as recommendation
    randoSong = func.getOneRandomSong(allSongs)

    
    #PLAYLIST COMPONENTS

    # Show Home page initially
    showHomePage()
    
    # Start the GUI event loop
    root.mainloop()
   
   
    # Checks if the user answers are captured correctly
    '''
    # For the checkboxes
    for x in checkVar:
      print(x.get())
    
    # For the slider year
    slide = func.sliderYear
    for x in slide:
        print(x)
    
    # For the radio Buttons   
    for x in radioChosenAnswers:
        print(x.get())
    '''
    
    
main()

