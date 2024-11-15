import tkinter as tk
import math
import numpy as np

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
            quizLabel.config(text="You selected: " + " ".join(answer))

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
    maxNum = 10000
    minNum = -10000
    questions = [
        {
            "question": "Which of the following would you like to be real? (You can choose more than one)",
            "questionType": "Checkboxes",
            "answer": ["Dragon", "Unicorn", "Mermaid", "Fairy", "Goblin", "Troll", "Phoenix"],
            "category": "Genre",
            "attribute": ["Pop", "Folk/Acoustic", "Jazz", "Metal", "R&B", "Blues", "World/Traditional"]
        },
        {
            "question": "If you could time travel, where would you go? (You can choose more than one)",
            "questionType": "Checkboxes",
            "answer": ["Dinosaur age", "Ancient Egypt", "Medieval Europe", "Future dystopia", "Pirate era", "Space exploration", "Fantasy world"],
            "category": "Genre",
            "attribute": ["Country", "Easy Listening", "Rock", "Dance/Electronic", "Hip Hop", "Latin", "Classical"]
        },
        {
            "question": "What year would you like to revisit?",
            "questionType": "Slider",
            "answer": [1998, 2020],
            "category": "Song Year Interval",
            "attribute": [np.arange(1998-2009), np.arange(2010-2020)]
        },
        {
            "question": "Which party game would you rather play?",
            "questionType": "Radiobuttons",
            "answer": ["Monopoly", "Uno", "Charades", "Pictionary"],
            "category": "Song Length",
            "attribute": [np.arange(113000, 170000), np.arange(170000, 256000), np.arange(256000, 384000), np.arange(384000, 485000)] # measured in ms
        },
        {
            "question": "Which emoji are you?",
            "questionType": "Radiobuttons",
            "answer": ["😂", "💀", "😑", "😏"],
            "category": "Popularity",
            "attribute": [np.arange(77, 89), np.arange(26, 56), np.arange(0, 25), np.arange(57, 77)]
        },
        {
            "question": "Would you rather not have hands or feet?",
            "questionType": "Radiobuttons",
            "answer": ["Hands", "Feet"],
            "category": "Danceability",
            "attribute": [np.arange(0.67, maxNum), np.arange(minNum, 0.67)]
        },
        {
            "question": "What’s your go to drink?",
            "questionType": "Radiobuttons",
            "answer": ["Coffee", "Tea", "Water", "Energy Drinks", "Alcohol"],
            "category": "Energy",
            "attribute": [np.arange(0.2, maxNum), np.arange(0.2, 0.7), np.arange(0.2, 1), np.arange(0.3, maxNum), np.arange(minNum, 0.5)]
        },
        {
            "question": "Out of these options, which one would you choose to wake you up for the rest of your life? (They could happen at any time)",
            "questionType": "Radiobuttons",
            "answer": ["Standard alarm sound", "Metal Pipe falling sound effect", "Fire Alarm"],
            "category": "Speechness",
            "attribute": [] #How to set attributes here?
        },
        {
            "question": "Imagine you are talking with someone, then you zone out. How would you respond?",
            "questionType": "Radiobuttons",
            "answer": ["Huh", "What", "Can you say that again", "Respond with “Yea” while nodding your head and pretend you heard them"],
            "category": "Genre",
            "attribute": ["Pop", "Folk/Acoustic", "Jazz", "Metal", "R&B", "Blues", "World/Traditional"]
        },
        {
            "question": "Are you happy?",
            "questionType": "Radiobuttons",
            "answer": ["Yes", "No"],
            "category": "Valence",
            "attribute": [np.arange(0.5, maxNum), np.arange(minNum, 0.5)]
        },
        {
            "question": "What would you rather be doing right now?",
            "questionType": "Radiobuttons",
            "answer": ["Sleeping", "Hanging out with Friends", "Watching your favorite show/movie", "Doing your hobby"],
            "category": "Tempo",
            "attribute": [np.arange(minNum, 100), np.arange(100, 211), np.arange(60, 120), np.arange(80, 160)]
        },
    ]

    #Create frames for each question
    quizFrames = []

    for question in questions:
        #Answer Default Value
        ans = tk.StringVar(value=None)

        #Add frame
        quiz = tk.Frame(root)
        question_label = tk.Label(quiz, text=question['question'], font=("Georgia", 14))
        question_label.pack(anchor='w', pady=20, padx=20)

        quizLabel = tk.Label(quiz, text="Please make a selection", font=("Lucida Sans", 12))

        #if radio button:
        if question['questionType'] == "Radiobuttons":
            for answer in question['answer']:
                radio_button = tk.Radiobutton(quiz, text=answer, font=("Lucida Sans", 12), variable=ans, value=answer, command=selectOption(question['questionType']))
                radio_button.pack(anchor='w', pady=5, padx=20)
        elif question['questionType'] == "Checkboxes":
            selected = []
            for answer in question['answer']:
                checkbox = tk.Checkbutton(quiz, text=answer, font=("Lucida Sans", 12), variable=answer, command=selectOption(question['questionType']))
                checkbox.pack(anchor='w', pady=5, padx=20)
                selected.append(ans)
        elif question['questionType'] == "Slider":
            # sliderLabel = tk.Label(quiz, text="Slider questions not ready yet", font=("Lucida Sans", 12))
            # sliderLabel.pack(pady=10)
            slider = tk.Scale(quiz, variable=ans, from_=(question['answer'][0]), to=(question['answer'][1]), orient="horizontal")
            slider.pack(pady=5, padx=20)

        # Show answer
        quizLabel.pack(pady=10)
        quizFrames.append(quiz)

        nextButton = tk.Button(quiz, text="Next", command=lambda index=len(quizFrames)-1: goNext(index), bg='black', fg='white', font=("Lucida Sans", 14), padx=5, pady=5)
        backButton = tk.Button(quiz, text="Back", command=lambda index=len(quizFrames)-1: goBack(index), bg='black', fg='white', font=("Lucida Sans", 14), padx=5, pady=5)

        nextButton.pack(side="right", padx=75, pady=5)
        backButton.pack(side="left", padx=75, pady=5)
    
    #SEARCH COMPONENTS

    #RANDOM SONG COMPONENTS

    #PLAYLIST COMPONENTS

    # Show Home page initially
    showHomePage()
    
    # Start the GUI event loop
    root.mainloop()

main()