import tkinter as tk
import math
import numpy as np
import functions as func
import mongodbConnect as mdb
def main():
    def showHomePage():
        home.pack(fill="both", expand=True)
        search.pack_forget()
        randomSong.pack_forget()
        playlist.pack_forget()
        if quizFrames:
            for frame in quizFrames:
                frame.pack_forget()

    def showQuiz():
        home.pack_forget()
        search.pack_forget()
        randomSong.pack_forget()
        playlist.pack_forget()
        if quizFrames:
            quizFrames[0].pack(fill="both", expand=True)

    def showSearch():
        search.pack(fill="both", expand=True)
        home.pack_forget()
        randomSong.pack_forget()
        playlist.pack_forget()
        if quizFrames:
            for frame in quizFrames:
                frame.pack_forget()

    def showRandomSong():
        randomSong.pack(fill="both", expand=True)
        home.pack_forget()
        search.pack_forget()
        playlist.pack_forget()
        if quizFrames:
            for frame in quizFrames:
                frame.pack_forget()

    def showPlaylist():
        playlist.pack(fill="both", expand=True)
        home.pack_forget()
        search.pack_forget()
        randomSong.pack_forget()
        if quizFrames:
            for frame in quizFrames:
                frame.pack_forget()

    def selectOption(questionType):
        if questionType == "Radiobuttons":
            quizLabel.config(text="You selected: " + str(ans.get()))
        elif questionType == "Slider":
            quizLabel.config(text="You selected: " + str(ans.get()))

        #Add to list of calculations and calculate at end
        # if selectedAnswers[index]:
        #     selectedAnswers[index] = str(ans.get())
        # else:
        #     selectedAnswers.append(str(ans.get()))

    def selectCheckbox(cVariables):
        labelString = "You selected: \n"
        selectedChecks = []
        for index, var in enumerate(cVariables):
            if var.get():
                labelString += str(question["answer"][index]) + "\n"
                selectedChecks.append(question["answer"][index])
        quizLabel.config(text=labelString)

        #Add to list of calculations and calculate at end
        # if selectedAnswers[index]:
        #     selectedAnswers[index] = selectedChecks
        # else:
        #     selectedAnswers.append(selectedChecks)

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

    #Temp Function to check if the Querying works
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
        songs = mdb.find_all(query)
        print("----Works-----")
    
    
    #Functions in the Search Frame   
    def addDropdownGenres():
        addGenreSearch.add(chosenGenre.get())
        print(addGenreSearch)
    
    def deleteList():
        addGenreSearch.clear()
        print(addGenreSearch)
    
    #Submit button for song and artist search
    def submit():
        print(songSearched.get())
        print(artistSearched.get())
    
    #Submit button for Song options in Search WIP:
    def submitSearchOptions():
        pass
    
    def goSearch():
        #search for the songs based on input
        #replace this code with searching function:
        home.pack(fill="both", expand=True)
        search.pack_forget()
        randomSong.pack_forget()
        playlist.pack_forget()
        if quizFrames:
            for frame in quizFrames:
                frame.pack_forget()


    root = tk.Tk()
    root.title("Truify")
    #what size window do we need?
    root.geometry("600x600")

    #Frames for each page
    home = tk.Frame(root)
    search = tk.Frame(root)
    randomSong = tk.Frame(root)
    playlist = tk.Frame(root)

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
            "question": "Which of the following would you like to be real? (You can choose more than one)",
            "questionType": "Checkboxes",
            "answer": ["Dragon", "Unicorn", "Mermaid", "Fairy", "Goblin", "Troll", "Phoenix"],
            "category": "Genre",
            "attribute": ["pop", "Folk/Acoustic", "jazz", "metal", "R&B", "blues", "World/Traditional"]
        },
        {
            "question": "If you could time travel, where would you go? (You can choose more than one)",
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
            "question": "Out of these options, which one would you choose to wake you up for the rest of your life? (They could happen at any time)",
            "questionType": "Radiobuttons",
            "answer": ["Standard alarm sound", "Metal Pipe falling sound effect", "Fire Alarm"],
            "category": "Loudness",
            "attribute": ["-16,-0.1", "-0.14, -0.2", "-20.6,-3"] #DECIDED NOT USE FOR QUERY
        },
        {
            "question": "Imagine you are talking with someone, then you zone out. How would you respond?",
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
            
            button = tk.Button(quiz, text="Make Query", command=printQuery)
            button.pack()
        elif question['questionType'] == "Checkboxes":
            for answer in question['answer']:
                var = tk.StringVar(value=0)
                #Stores the values of the user into list
                checkVar.append(var)
                checkbox = tk.Checkbutton(quiz, text=answer, font=("Lucida Sans", 12), variable=var, onvalue=answer, offvalue="Nothing", command=selectOption(question['questionType']))
                checkbox.pack(anchor='w', pady=5, padx=20)
                
        elif question['questionType'] == "Slider":
            # sliderLabel = tk.Label(quiz, text="Slider questions not ready yet", font=("Lucida Sans", 12))
            # sliderLabel.pack(pady=10)
            sliderVar = tk.IntVar(value=None)
            slider = tk.Scale(quiz, variable=sliderVar, from_=(question['answer'][0]), to=(question['answer'][1]), orient="horizontal",)
            slider.pack(pady=5, padx=20)
            
            #Used to update the slider
            submitbutton = tk.Button(quiz, text="Submit the Year", command=lambda: func.updateYear(slider))
            submitbutton.pack()
            
        # Show answer
        quizLabel.pack(pady=10)
        quizFrames.append(quiz)

        nextButton = tk.Button(quiz, text="Next", command=lambda index=len(quizFrames)-1: goNext(index), bg='black', fg='white', font=("Lucida Sans", 14), padx=5, pady=5)
        backButton = tk.Button(quiz, text="Back", command=lambda index=len(quizFrames)-1: goBack(index), bg='black', fg='white', font=("Lucida Sans", 14), padx=5, pady=5)

        nextButton.pack(side="right", padx=75, pady=5)
        backButton.pack(side="left", padx=75, pady=5)
        
 
    #The options avaliable for the Search Page
    searchInputComponents = [
        {
          "id": 1,
          "genre": ["pop","Folk/Acoustic","jazz","metal",
                    "R&B","blues","World/Traditional","country",
                    "easy listening","rock","Dance/Electronic",
                    "hip hop","latin","classical"]  
        },
        {
            "id": 2,
            "year": ["Min Year", "Max Year"] 
        },
        {
            "id": 3,
            "length" : ["Min Length:", "Max Length"]
        },
        {
            "id": 4,
            "PopularityandDance": ["Max Popularity", "Max Danceabilty"]
        },
        {
            "id": 5,
            "EnergyandTempo": ["Max Energy", "Max Tempo"]
        }
    ]
    
    
    
    #SEARCH COMPONENTS
    titleRow = 0
    titleCol = 0
    #Home button
    homeButton = tk.Button(search, text="Home", command=showHomePage, bg='white', fg='black', font=("Lucida Sans", 12))
    homeButton.grid(sticky = "w", row = titleRow, column = titleCol, pady=20, padx=20, columnspan = 100)

    #Search label
    searchTitle = tk.Label(search, text="Search", font=("Georgia", 25, "bold"))
    searchTitle.grid(row = titleRow, column = titleCol, pady=5, padx=20, columnspan = 100)

    # which types are these?
    genreOptions = [
        "A genre",
        "another genre"
    ]
    genre = tk.StringVar()
    genre.set("Please select a genre")
    minYear = tk.IntVar()
    minLength = tk.IntVar()
    maxPopularity = tk.IntVar()
    maxEnergy = tk.IntVar()
    maxYear = tk.IntVar()
    maxLength = tk.IntVar()
    maxDanceability = tk.IntVar()
    maxTempo = tk.IntVar()
    searchSong = tk.StringVar()
    searchArtist = tk.StringVar()
    
    genreInput = tk.OptionMenu(search, genre, *genreOptions)
    genreInput.config(bg="black", fg="white", font=("Lucida Sans", 12))
    minYearLabel = tk.Label(search, text="Min year:", font=("Lucida Sans", 12))
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

    searchSongLabel = tk.Label(search, text="Search Song:", font=("Lucida Sans", 12))
    searchSongInput = tk.Entry(search, textvariable=searchSong, bg='black', fg='white')

    searchArtistLabel = tk.Label(search, text="Search Artist:", font=("Lucida Sans", 12))
    searchArtistInput = tk.Entry(search, textvariable=searchArtist, bg='black', fg='white')

    genreRow = titleRow + 1
    genreCol = titleCol
    genreInput.grid(row = genreRow, column = genreCol, columnspan = 100, padx = 15, pady = 25)

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

    searchSongRow = mERow + 1
    searchSongCol = mPCol
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

