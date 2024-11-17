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
        elif questionType == "Checkboxes":
            quizLabel.config(text="You selected: ".join(answer))

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
        question_label = tk.Label(quiz, text=question['question'], font=("Georgia", 14))
        question_label.pack(anchor='w', pady=20, padx=20)

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
        
    
    #SEARCH COMPONENTS

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

