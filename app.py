# Justin Caringal, Lanz Dungo, Akansha Negi, Julian Williams
# CS 430, Dr. Charles Yu
# 
# The main application for interfacing with the Truify Discography Database

import tkinter as tk
from tkinter import messagebox
import math
import numpy as np
import functions as func
import mongodbConnect as mdb
import random
import string

# libraries that help set up Spotify API server
import os
import json
import webbrowser as wb
from multiprocessing import Process
from dotenv import load_dotenv, find_dotenv
from access_spotify import app
from extract_songs import extract_songs
LOCALHOST = 'http://127.0.0.1:5000/'

error_displayed = func.error_displayed

def main():
    def showHomePage():
        home.pack(fill="both", expand=True)
        search.pack_forget()
        randomSong.pack_forget()
        #playlist.pack_forget()
        quizResults.pack_forget()
        searchResults.pack_forget()
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
        #playlist.pack_forget()
        quizResults.pack_forget()
        searchResults.pack_forget()
        if quizFrames:
            quizFrames[0].pack(fill="both", expand=True)

    def showQuizResults():
        quizResults.pack(fill="both", expand=True)
        home.pack_forget()
        search.pack_forget()
        randomSong.pack_forget()
        #playlist.pack_forget()
        searchResults.pack_forget()
        if quizFrames:
            for frame in quizFrames:
                frame.pack_forget()

    def showSearch():
        search.pack(fill="both", expand=True)
        home.pack_forget()
        randomSong.pack_forget()
        #playlist.pack_forget()
        quizResults.pack_forget()
        searchResults.pack_forget()
        if quizFrames:
            for frame in quizFrames:
                frame.pack_forget()

    def showRandomSong():
        randomSong.pack(fill="both", expand=True)
        home.pack_forget()
        search.pack_forget()
        #playlist.pack_forget()
        quizResults.pack_forget()
        searchResults.pack_forget()
        if quizFrames:
            for frame in quizFrames:
                frame.pack_forget()

        displayString.set("")
        randCounter = 0

    #Not enough time
    '''
    def showPlaylist():
        playlist.pack(fill="both", expand=True)
        home.pack_forget()
        search.pack_forget()
        randomSong.pack_forget()
        quizResults.pack_forget()
        searchResults.pack_forget()
        if quizFrames:
            for frame in quizFrames:
                frame.pack_forget()
    '''

    def showSearchResults():
        searchResults.pack(fill="both", expand=True)
        home.pack_forget()
        search.pack_forget()
        randomSong.pack_forget()
        quizResults.pack_forget()
        #playlist.pack_forget
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
    #If so creates/ shows the result page
    def checkQuiz():
        quizState["valid"] = func.checkQuizValid(checkVar, radioChosenAnswers)
        print("Quiz valid state:", quizState["valid"])
        
        if quizState["valid"]:
            # Fetch songs based on quiz
            quizState["songsFromQuiz"] = printQuery() or [] 
            print("Songs from Quiz:", quizState["songsFromQuiz"])
            
            # Initialize lists for song properties
            title, artist, release_date, genresForQuiz = [], [], [], []
            
            # Populate lists with song data if available
            for song in quizState["songsFromQuiz"]:
                title.append(song.get("song", "N/A"))  # Default to "N/A" if field is missing
                artist.append(song.get("artist", "Unknown"))
                release_date.append(song.get("year", "Unknown"))
                genresForQuiz.append(song.get("genre", ["Unknown"]))
    
            # Make sure there are at least 10 song suggestions by filling with placeholders
            while len(title) < 10:
                title.append(f"Song {len(title) + 1}")
                artist.append("Placeholder Artist")
                release_date.append("Unknown Date")
                genresForQuiz.append(["Placeholder Genre"])
    
            # Create the list of song suggestions
            songSuggestions = [
                {
                    "title": title[i],
                    "artist": artist[i],
                    "release_date": release_date[i],
                    "genre": genresForQuiz[i]
                }
                for i in range(len(title))
            ]
    
            # Starting index for pagination
            startIndex = 0
    
            def loadSongs(startIndex):
                # Clear the current frame content
                for frame in quizResults.winfo_children():
                    frame.grid_forget()

                # Set the current row to start rendering songs
                quizTitleRow = 0
                quizTitleCol = 0
                currentRow = quizTitleRow + 1

                # Home button
                quizHomeButton = tk.Button(quizResults, text="Home", command=showHomePage, bg='white', fg='black', font=("Lucida Sans", 12))
                quizHomeButton.grid(sticky="w", row=quizTitleRow, column=quizTitleCol, pady=20, padx=20)

                # Quiz results label
                quizResultsTitle = tk.Label(quizResults, text="Song Suggestions", font=("Georgia", 25, "bold"))
                quizResultsTitle.grid(row=quizTitleRow, column=quizTitleCol + 1, pady=5, padx=20, columnspan=100)

                # Loop through and load the current set of songs
                for i in range(startIndex, min(startIndex + 4, len(songSuggestions))):
                    song = songSuggestions[i]
                    column = (i % 2)
                    songName = tk.Label(quizResults, text=f"{i + 1}. {song['title']}", font=("Lucida Sans", 14, "bold"))
                    songName.grid(row=currentRow, column=column * 2, pady=(25, 10), padx=20)

                    artistName = tk.Label(quizResults, text=f"Artist: {song['artist']}", font=("Lucida Sans", 12))
                    artistName.grid(row=currentRow + 1, column=column * 2, pady=5, padx=20)

                    releaseName = tk.Label(quizResults, text=f"Release Date: {song['release_date']}", font=("Lucida Sans", 12))
                    releaseName.grid(row=currentRow + 2, column=column * 2, pady=5, padx=20)

                    genreName = tk.Label(quizResults, text=f"Genre: {', '.join(song['genre'])}", font=("Lucida Sans", 12))
                    genreName.grid(row=currentRow + 3, column=column * 2, pady=5, padx=20)

                    # Move to the next row only after the second column
                    if column == 1:
                        currentRow += 5

                # Ensure buttons are always at the bottom
                lastRow = currentRow + 5

                # Add "Next" button
                if startIndex + 4 < len(songSuggestions):
                    nextSongsButton = tk.Button(quizResults, text="Next", command=lambda: loadNextFrame(startIndex, startIndex + 4), bg='black', fg='white', font=("Lucida Sans", 14))
                    nextSongsButton.grid(row=lastRow, column=1, pady=20, padx=20)

                # Add "Back" button
                if startIndex > 0:
                    backSongsButton = tk.Button(quizResults, text="Back", command=lambda: loadNextFrame(startIndex, startIndex - 4), bg='black', fg='white', font=("Lucida Sans", 14))
                    backSongsButton.grid(row=lastRow, column=0, pady=20, padx=20)
    
            def loadNextFrame(startIndex, newStartIndex):
                loadSongs(newStartIndex)
    
            # Load the first set of songs
            loadSongs(startIndex)
            showQuizResults()
        else:
            print("The quiz is invalid or not completed. Please try again.")

    
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

        songs_dict = {
            'songs' : extract_songs(songs),
        }
        print('LOOK AT MEEEEEE', songs, type(songs))
        load_dotenv(find_dotenv())
        json_path = os.getenv('DATA_TRANSFER_JSON')
        with open(json_path, 'w') as transfer_file:
            json.dump(songs_dict, transfer_file)
        wb.open(LOCALHOST)
        return songs
    
    #Functions in the Search Frame   
    def addDropdownGenres():
        if genre.get() != "Select a Genre":
            addGenreSearch.add(genre.get())
        print(addGenreSearch)
    
    def deleteList():
        addGenreSearch.clear()
        print(addGenreSearch)
    

    def submitSearchOptions():
        VALIDITYINDEX = 0
        QUERYRESULT = 1

        # Hold All Filter Choices
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

            # Check if the query is valid
            if results[VALIDITYINDEX] == True:
                print("Query is valid")
                songs = mdb.getSearchFilterQuery(results[QUERYRESULT])

                # Call function to display song results
                displaySongResults(songs)
            else:
                print("Something went wrong")
                pass

        except Exception as e:
            print("An unexpected error occurred:", e)
            messagebox.showerror("Error", "You entered a value that is not a number. OR You have not set a Max Year and Max Length")

    def displaySongResults(songs):
        """
        Function to display the results of the filtered song search.
        It will display song name and artist only.
        """
        print(f"Displaying search results for {len(songs)} songs")

        # Clear previous content in the searchResults frame
        for widget in searchResults.winfo_children():
            widget.grid_forget()  # Removes widgets managed by grid

        # Create a container frame for the list of songs
        resultsFrame = tk.Frame(searchResults, bg='#f5f5f5', padx=20, pady=20)
        resultsFrame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # Use grid for positioning the frame

        # Adjust column/row weights for centering and scrolling
        searchResults.grid_rowconfigure(0, weight=1, minsize=100)
        searchResults.grid_columnconfigure(0, weight=1)

        # Create a canvas for scrolling if there are many songs
        canvas = tk.Canvas(resultsFrame)
        scroll_y = tk.Scrollbar(resultsFrame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll_y.set)

        # Create a frame within the canvas for the actual song labels
        songListFrame = tk.Frame(canvas, bg='#f5f5f5')

        # Add the song list frame to the canvas
        canvas.create_window((0, 0), window=songListFrame, anchor="nw")

        # Pack the canvas and scrollbar within the resultsFrame
        canvas.grid(row=0, column=0, sticky="nsew")  # Stretch the canvas horizontally and vertically
        scroll_y.grid(row=0, column=1, sticky="ns")  # Stretch the scrollbar vertically

        # Populate the song labels with numbers on the side
        for idx, song in enumerate(songs, start=1):
            # Create a label for each song with a number on the left
            songText = f"{idx}. {song['song']} by {song['artist']}"
            songLabel = tk.Label(songListFrame, text=songText, font=("Lucida Sans", 14), bg='#f5f5f5', anchor="w", padx=10, pady=10)

            # Add a hover effect to the song labels for better interactivity
            songLabel.bind("<Enter>", lambda event, label=songLabel: label.config(bg="#e0e0e0"))
            songLabel.bind("<Leave>", lambda event, label=songLabel: label.config(bg="#f5f5f5"))

            songLabel.grid(row=idx-1, column=0, sticky="w", padx=10, pady=5)  # Using grid instead of pack

        # Update the scroll region to fit the content
        songListFrame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Home Button (using grid for layout)
        homeButton = tk.Button(searchResults, text="Back", command=showHomePage, bg="black", fg="white", font=("Lucida Sans", 14))
        homeButton.grid(row=1, column=0, pady=10, sticky="nsew")  # Placed below the song list and stretches across

        showSearchResults()


    def goSearch():
        # Get user input for song and artist
        searchedSong = searchSong.get()
        searchedArtist = searchArtist.get()

        # Validate the inputs
        querySongArtist, optionChosen = func.valdititySongArtistSubmit(searchedSong, searchedArtist)

        if not querySongArtist:
            print("Something went wrong")
        else: 
            # Query the database to fetch filtered results
            songFromFilter = mdb.getSearchFilterQuery(querySongArtist)

            # Check if results were found
            if songFromFilter:
                # Clear previous search results
                for widget in searchResults.winfo_children():
                    widget.grid_forget()  # or widget.pack_forget() depending on how you are packing widgets

                if optionChosen == 'song':
                    # Show the page for the single song
                    song = songFromFilter[0]  # Get the first (and only) song result
                    displaySingleSongPage(song)  # Implement this function to display details of the song
                else:
                    # Show the page of multiple songs from the artist
                    displayArtistSongsPage(songFromFilter)  # Implement this function to display a list of songs

                print("Search results displayed")
            else:
                # Handle no results
                print("No matching songs found")

    def displaySingleSongPage(song):
        """
        Function to display the details of a single song.
        This is used within the search page
        """
        print(f"Displaying song details for: {song['song']} by {song['artist']}")

        # Create a container frame for centering the content
        songDetailsFrame = tk.Frame(searchResults, bg='#f5f5f5', padx=20, pady=20)

        # Song name and artist
        songDetailsLabel = tk.Label(songDetailsFrame, text=f"Song: {song['song']}", font=("Georgia", 16, "bold"), bg='#f5f5f5', anchor="center")
        songDetailsLabel.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)

        artistDetailsLabel = tk.Label(songDetailsFrame, text=f"Artist: {song['artist']}", font=("Lucida Sans", 14), bg='#f5f5f5', anchor="center")
        artistDetailsLabel.grid(row=2, column=1, sticky="nsew", padx=10, pady=5)

        # Year, Genre, Duration
        yearDetailsLabel = tk.Label(songDetailsFrame, text=f"Year: {song.get('year', 'N/A')}", font=("Lucida Sans", 12), bg='#f5f5f5', anchor="center")
        yearDetailsLabel.grid(row=3, column=1, sticky="nsew", padx=10, pady=5)

        genreDetailsLabel = tk.Label(songDetailsFrame, text=f"Genre: {song.get('genre', 'N/A')}", font=("Lucida Sans", 12), bg='#f5f5f5', anchor="center")
        genreDetailsLabel.grid(row=4, column=1, sticky="nsew", padx=10, pady=5)

        # Convert duration from ms to seconds
        duration_seconds = song.get('duration_ms', 0) // 1000
        durationDetailsLabel = tk.Label(songDetailsFrame, text=f"Duration: {duration_seconds} seconds", font=("Lucida Sans", 12), bg='#f5f5f5', anchor="center")
        durationDetailsLabel.grid(row=5, column=1, sticky="nsew", padx=10, pady=5)

        # Center the entire song details frame within the parent window
        songDetailsFrame.grid(row=0, column=1, sticky="nsew")

        # Adjust column/row weight for centering
        searchResults.grid_rowconfigure(0, weight=1, minsize=100)
        searchResults.grid_columnconfigure(0, weight=1)  # Empty column on the left
        searchResults.grid_columnconfigure(1, weight=1)  # Middle column for content
        searchResults.grid_columnconfigure(2, weight=1)  # Empty column on the right

        # Create the Home (Back) button at the bottom
        homeButton = tk.Button(searchResults, text="Back", command=showHomePage, bg="black", fg="white", font=("Lucida Sans", 14))
        homeButton.grid(row=1, column=1, sticky="nsew", pady=(10, 20))  # Place it below the content frame

        # Show the updated content
        showSearchResults()


    def displayArtistSongsPage(songs):
        """
        Function to display a list of songs from an artist.
        This would involve showing the song names and artists in a numbered list.
        """
        print(f"Displaying songs by artist: {songs[0]['artist']}")

        # Create a frame to hold the list of songs
        artistSongsFrame = tk.Frame(searchResults, bg='#f5f5f5', padx=20, pady=20)
        artistSongsFrame.pack(fill="both", expand=True, pady=(0, 20))  # Ensure the frame is packed with bottom padding

        # Create a canvas for scrolling if there are many songs
        canvas = tk.Canvas(artistSongsFrame)
        scroll_y = tk.Scrollbar(artistSongsFrame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll_y.set)

        # Create a frame within the canvas for the actual song labels
        songListFrame = tk.Frame(canvas, bg='#f5f5f5')

        # Add the song list frame to the canvas
        canvas.create_window((0, 0), window=songListFrame, anchor="nw")

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        # Populate the song labels with numbers on the side
        for idx, song in enumerate(songs, start=1):
            # Create a label for each song with a number on the left
            songText = f"{idx}. {song['song']} by {song['artist']}"
            songLabel = tk.Label(songListFrame, text=songText, font=("Lucida Sans", 14), bg='#f5f5f5', anchor="w", padx=10, pady=10)

            # Add a hover effect to the song labels for better interactivity
            songLabel.bind("<Enter>", lambda event, label=songLabel: label.config(bg="#e0e0e0"))
            songLabel.bind("<Leave>", lambda event, label=songLabel: label.config(bg="#f5f5f5"))

            songLabel.pack(fill="x", pady=5)

        # Update the scroll region to fit the content
        songListFrame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Create the Home (Back) button
        homeButton = tk.Button(searchResults, text="Back", command=showHomePage, bg="black", fg="white", font=("Lucida Sans", 14))
        homeButton.pack(side="bottom", pady=10) 

        # Show the updated content
        showSearchResults()



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
    #playlist = tk.Frame(root) Not enough time
    quizResults = tk.Frame(root)
    searchResults = tk.Frame(root)

    #HOME PAGE COMPONENTS
    truifyLabel = tk.Label(home, text="Truify", font=("Lucida Sans", 24, "bold"))
    quizButton = tk.Button(home, text="Quiz", command=showQuiz, bg='black', fg='white', font=("Georgia", 18, "bold"), padx=10, pady=10)
    searchButton = tk.Button(home, text="Search", command=showSearch, bg='black', fg='white', font=("Georgia", 18, "bold"), padx=10, pady=10)
    randomButton = tk.Button(home, text="Random Song", command=showRandomSong, bg='black', fg='white', font=("Georgia", 18, "bold"), padx=10, pady=10)
    #playlistButton = tk.Button(home, text="Playlist", command=showPlaylist, bg='black', fg='white', font=("Georgia", 18, "bold"), padx=10, pady=10)

    # Place in frames
    truifyLabel.pack(pady=20)
    quizButton.pack(pady=10)
    searchButton.pack(pady=10)
    randomButton.pack(pady=10)
    #playlistButton.pack(pady=10)
    
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

    #Trackes whether the quiz is valid or not
    quizState = {
        "valid": False,
        "songsFromQuiz": None,
    }
    
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
    global randCounter
    randCounter = 0
    global targetString
    targetString = ""
    allSongs = mdb.getAllSongs()
    song = None
    displayString = tk.StringVar()
    
    def _randomize():
        global randCounter
        global targetString
        
        if randCounter == 0:
            song = func.getOneRandomSong(allSongs)
            targetString = f"\"{song['song']}\"\n\n{song['artist']}"
            displayString.set(targetString)
    
        s = list(displayString.get())
        s[randCounter] = targetString[randCounter]   
        randCounter += 1
        for i in range(randCounter, len(targetString)):
            if s[i].isspace() or s[i] == "\"":
                continue    
            s[i] = random.choice(string.ascii_letters)
        displayString.set("".join(s))

        if randCounter < len(targetString):
            root.after(50, _randomize)
        else:
            randCounter = 0

    def randomize():
        global randCounter
        if randCounter == 0:
            _randomize()
    
    title = tk.Label(
        randomSong,
        text="Song Randomizer",
        font=("Lucida Sans", 32)
    ).pack(pady=10)

    displayLabel = tk.Label(
        randomSong,
        textvariable=displayString,
        font=("Consolas", 20)
    ).pack(pady=80)

    randButton = tk.Button(
        randomSong,
        text="Randomize!",
        command=randomize,
        bg="black", fg="white", font=("Lucida Sans", 14)
    ).pack(ipadx=20, ipady=10)
    
    backButton = tk.Button(
        randomSong,
        text="Back",
        command=showHomePage,
        bg="black", fg="white", font=("Lucida Sans", 14)
    ).pack(side="bottom", pady=10)
    

    # NOT ENOUGH TIME TO DO
    '''
    #PLAYLIST COMPONENTS
    playlistResults = [
        {"song": "a song", "artist": "an artist"},
        {"song": "another song", "artist": "another artist"},
        {"song": "third song", "artist": "third artist"},
        {"song": "fourth song", "artist": "fourth artist"},
        {"song": "fifth song", "artist": "fifth artist"},
        {"song": "sixth song", "artist": "sixth artist"},
        {"song": "seventh song", "artist": "seventh artist"},
        {"song": "eighth song", "artist": "eighth artist"},
        {"song": "ninth song", "artist": "ninth artist"},
        {"song": "tenth song", "artist": "tenth artist"},
        {"song": "eleventh song", "artist": "eleventh artist"},
        {"song": "twelfth song", "artist": "twelfth artist"},
        {"song": "thirteenth song", "artist": "thirteenth artist"},
        {"song": "fourteenth song", "artist": "fourteenth artist"},
        {"song": "fifteenth song", "artist": "fifteenth artist"},
        {"song": "sixteenth song", "artist": "sixteenth artist"},
        {"song": "seventeenth song", "artist": "seventeenth artist"},
        {"song": "eighteenth song", "artist": "eighteenth artist"},
        {"song": "nineteenth song", "artist": "nineteenth artist"},
        {"song": "twentieth song", "artist": "twentieth artist"}
    ]

    plCurrentFrame = 0
    plResults = 10

    # Display search results per page
    def displayPlaylistResults(page):
        # Clear frames
        for widget in playlist.winfo_children():
            widget.grid_forget()

        # Start and end index for current page
        startIndex = page * plResults
        endIndex = min(startIndex + plResults, len(playlistResults))
        playlistRow = 0
        playlistCol = 0

        # Home button
        plHomeButton = tk.Button(playlist, text="Home", command=showHomePage, bg='white', fg='black', font=("Lucida Sans", 12))
        plHomeButton.grid(row=playlistRow, column=playlistCol, pady=20, padx=20, sticky="w", columnspan=100)

        # playlist title
        plTitle = tk.Label(playlist, text="Spotify Playlist", font=("Georgia", 25, "bold"))
        plTitle.grid(row=playlistRow, column=playlistCol + 1, pady=5, padx=20, columnspan=100, sticky="NESW")
        playlistRow += 1

        if len(playlistResults) > 0:
            # Display results for current page
            for i, result in enumerate(playlistResults[startIndex:endIndex]):
                # Result label
                songLabel = tk.Label(playlist, text=f"{startIndex + i + 1}. {result['song']} by {result['artist']}", font=("Lucida Sans", 12), pady=10, padx=30)
                songLabel.grid(row=playlistRow, column=playlistCol, pady=2, padx=20, sticky="w")

                # Delete Button
                deleteButton = tk.Button(playlist, text="Delete", command=lambda index=startIndex + i: deleteSong(index), bg='red', fg='white', font=("Lucida Sans", 10))
                deleteButton.grid(row=playlistRow, column=playlistCol + 1, pady=10, padx=20, sticky="e", columnspan = 100)

                playlistRow += 1
        else:
            songLabel = tk.Label(playlist, text="No results found.", font=("Lucida Sans", 12), pady=10, padx=30)
            songLabel.grid(row=playlistRow, column=playlistCol, pady=2, padx=20, sticky="w")


        # Button row
        buttonRow = playlistRow
        buttonCol = playlistCol

        # Back Button
        if page > 0:
            plBack = tk.Button(playlist, text="Back", command=lambda: changePLFrame(page - 1, plCurrentFrame), bg='black', fg='white', font=("Lucida Sans", 14))
            plBack.grid(row=buttonRow, column=buttonCol, padx=75, pady=30, columnspan=2, sticky="w")

        # Next Button
        if endIndex < len(playlistResults):
            plNext = tk.Button(playlist, text="Next", command=lambda: changePLFrame(page + 1, plCurrentFrame), bg='black', fg='white', font=("Lucida Sans", 14))
            plNext.grid(row=buttonRow, column=buttonCol + 1, padx=75, pady=30, columnspan=2, sticky="e")

    # Delete 
    def deleteSong(index, playlistResults):
        playlistResults.pop(index) 
        playlistResults(plCurrentFrame) 

    def changePLFrame(page, plCurrentFrame):
        plCurrentFrame = page
        displayPlaylistResults(plCurrentFrame)

    displayPlaylistResults(plCurrentFrame)
    '''

    # Show Home page initially
    showHomePage()
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
    
if __name__ == '__main__':
    # starts up Spotify API server
    server = Process(target=app.run)
    server.start()

    # displays Truify GUI to user
    main()
