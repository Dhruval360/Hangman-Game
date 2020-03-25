#To make a hangman game
#Authors: Dhruval PB
import pandas as pd
import random
from tkinter import messagebox
from tkinter import *
import tkinter.messagebox
from tkinter import ttk
import os
HANGMAN = (
       """
       |    
       |
       |
       |
       |
       |
       |
       |
       ----------
       """,
       """
       ------
       |    
       |
       |
       |
       |
       |
       |
       |
       ----------
       """,
       """       
       ------
       |      |
       |
       |
       |
       |
       |
       |
       |
       ----------
       """,
       """
       ------
       |      |
       |     O
       |
       |
       |
       |
       |
       |
       ----------
       """,
       """
       ------
       |      |
       |     O
       |    -+-
       |
       |  
       |  
       |  
       |  
       ----------
       """,
       """
       ------
       |      |
       |     O
       |   /-+-
       |  
       |  
       |  
       |  
       |  
       ----------
       """,
       """
       ------
       |      |
       |     O
       |   /-+-/
       |  
       |  
       |  
       |  
       |  
       ----------
       """,
       """
       ------
       |      |
       |     O
       |   /-+-/
       |      |
       |      |  
       |  
       |  
       |  
       ----------
       """,
       """
       ------
       |      |
       |     O
       |   /-+-/
       |      |
       |      |
       |    |
       |    |
       |  
       ----------
       """,
       """
       ------
       |      |
       |     O
       |   /-+-/
       |      |
       |      |
       |    |  |
       |    |  |
       |  
       ----------
       """)  #Text art for hangman

script_dir = os.path.dirname(__file__) #This gives the absolute path of the directory the python code is in
rel_path = "IMDB-Movie-Data.csv" #This dataset was downloaded from kaggle
abs_file_path = os.path.join(script_dir, rel_path)

movie_df = pd.read_csv(abs_file_path)
gens = set(movie_df['Genre'])
gens.add('')
GENRES = sorted(gens)           

top= Tk()
top.title("Welcome")
top.geometry('340x400')

def link():
    root = Tk()
    
    #Variables
    submitted = set()
    clicked, diffclk = StringVar(), StringVar()
    bg = '#000000000'
    fg = '#000fff000'

    #Functions
    #Update function, to update the game outputs after each input
    def update():
        output.delete(0.0, END)
        output.insert(0.0, out)
        guess.add(key) #key is the virtual keyboard input
        gtn.delete(0.0, END)
        gtn.insert(0.0, guess)
    
    #For submit button
    def submission():
        try:
            gen = clicked.get()
            movies = list(movie_df.loc[movie_df['Genre'] == gen, 'Title'])
            
            global chosen
            chosen = random.choice(movies) # Chosen movie
            hint_df = movie_df.loc[movie_df['Title'] == chosen, 'Description':'Runtime (Minutes)']
            hintss = hint_df['Description']
            hint_actors = hint_df['Actors']
            hint_directors = hint_df['Director']
            #print(chosen)  #Uncomment this to get the correct answer on the terminal for your reference

            #Find a better method than slicing...
            global hint_desc
            hint_desc = str(hintss)[4:-32:1]
            global hint_actor
            hint_actor = str(hint_actors)[4:-27:1]
            global hint_director
            hint_director = str(hint_directors)[4:-30:1]
            
            chosen = chosen.upper()

            global all_letters
            all_letters = set(chosen)  # All the letters in that movie
            try:
                a.remove(" ") #To remove spaces if any
            except:
                pass
            
            global chosen_movie
            chosen_movie = list(map(lambda x: list(x), chosen.split()))  # Chosen movie split into its different words

            global out
            out = list(map(lambda x: ['_' for i in x], chosen_movie))  # Output shown each time we enter a letter

            all_alpha =  set(filter(lambda x: x.isalpha(), all_letters))  #To take a set of only alphabets
            
            global guess
            guess = set(random.sample(all_alpha, 2)) #To give 2 random letters in the beginning
            
            for j in all_letters:
              if not j.isalpha() or j in guess:
                for i in chosen_movie:
                    if j in i:
                        for a in range(len(i)):
                            if i[a] == j:
                                out[chosen_movie.index(i)][a] = j

            output.delete(0.0, END)
            output.insert(0.0, out)
            
            gtn.delete(0.0, END)
            gtn.insert(0.0, guess)

            difficulty = diffclk.get()
            if difficulty == 'Easy':
                l = ['*' for i in range(10)]
            elif difficulty == 'Medium':
                l = ['*' for i in range(7)]
            elif difficulty == 'Hard':
                l = ['*' for i in range(5)]
            global lives
            lives = l
            hang.delete(0.0, END)
            submitted.add(1)
        except:
            messagebox.showinfo('All fields not selected!!', 'Please click on the "submit" button after selecting your choices above')
    #For hintbutton
    def hintbut():
        if len(submitted)==0:
            messagebox.showinfo('Not submitted', 'Please click on the "submit" button after selecting your choices above')
        else:
            messagebox.showinfo( 'Hint', 'Description-{}\nActors-{}\nDirector-{}'.format(hint_desc, hint_actor, hint_director))

    #For each keyboard button
    def click(inp):
        global key
        key = inp
        if len(submitted)==1:
            if key not in guess:
                if key in all_letters:
                    for i in chosen_movie:
                        if key in i:
                            for a in range(len(i)):
                                if i[a] == key:
                                    out[chosen_movie.index(i)][a] = key
                    update()
                elif key not in all_letters and len(lives) != 0:
                    update()
                    lives.pop()
                    messagebox.showinfo('Letter absent',
                                        "\nThe letter '{}' is absent in the movie's name\nYou lost a life and now have only {} lives left".format(
                                            key, len(lives)))
                    hang.delete(0.0, END)
                    hang.insert(0.0, HANGMAN[-len(lives) - 1])
                    if len(lives)==0:
                        hang.delete(0.0, END)
                        hang.insert(0.0, HANGMAN[-len(lives) - 1])
                        messagebox.showinfo('Game Over', 'Oops! You have lost all your chances :(\nThe correct movie was: {}'.format(chosen))
                        messagebox.showinfo('Play again?', 'Better luck next time!!\nWould you like to play again?\nClick on the submit button after choosing another Genre of your taste')        
                        hang.delete(0.0, END)
                        output.delete(0.0, END)
                        output.insert(0.0, 'Click on submit after choosing the difficulty level and a genre of your choice.')
                        guess.clear()
                        submitted.pop()
                        gtn.delete(0.0, END)
                        gtn.insert(0.0, 'Click on submit to make any guesses.')
                        
            elif key in guess:
                messagebox.showinfo('Already used', 'You have already used that letter')

            if out == chosen_movie:
                update()
                messagebox.showinfo('You won!!', 'Yay! you won!\nCongratulations on guessing the right word!')
                messagebox.showinfo('Play again?', 'Would you like to play again?\nClick on the submit button after choosing another Genre of your taste')
                hang.delete(0.0, END)
                output.delete(0.0, END)
                output.insert(0.0, 'Click on submit after choosing the difficulty level and a genre of your choice.')
                guess.clear()
                submitted.pop()
                gtn.delete(0.0, END)
                gtn.insert(0.0, 'Click on submit to make any guesses.')

        else:
            messagebox.showinfo('Not submitted', 'Please click on the "submit" button after selecting your choices above')

    #For quit button
    def _quit():
        messagebox.askquestion('Quick Question', 'Thank you for using this application.\nDid you like it?')
        messagebox.showinfo('Thank you', 'Have a nice day!')
        root.quit()  # stops mainloop
        root.destroy()

    root.configure(background="black")
    root.geometry('660x620')

    #Title
    root.title("The Hangman Game")

    #Lists
    difflvl = ['', 'Easy', 'Medium', 'Hard']

    #Genres seletion
    genreslab = Label(root, text="Select the movie genres here:", font='system 16 bold', bg=bg, fg=fg)
    genreslab.place(x=5, y=60)
    genressel = ttk.OptionMenu(root, clicked, *GENRES)
    genressel.place(x=230, y=60)

    #Difficulty selection
    difflab = Label(root, text="Select the difficulty level here:", font=('system 16 bold'), bg=bg, fg=fg)
    difflab.place(x=5, y=120)
    diffsel = ttk.OptionMenu(root, diffclk, *difflvl)
    diffsel.place(x=230, y=120)

    #Hangman status
    hang = Text(root, width=20, height=13, font=('none 11 bold'), fg="#fff000000", bg='#111111111')
    hang.place(x=400, y=55)
    hang_status = Label(root, text='Hangman status', font='system 10 bold', bg=bg, fg='orange').place(x=425, y=55)

    #Output:
    Label(root,text="The movie you need to guess is:",font=('Time 15 bold'),bg='powder blue').place(x=5,y=250)
    output = Text(root, width=80, height=4, fg=bg, bg='Dark gray')
    output.place(x=5, y=290)
    output.insert(0.0, 'Click on the submit button after choosing the difficulty and genre of your \nchoice.')

    #Hint
    Label(root, text="Finding it difficult? Try taking a hint:", font=('none 12 bold'),bg='powder blue').place(x=0,y=370)
    Button(root,text="Hint",font=('none 12 bold'), command=hintbut).place(x=300,y=366)

    #Guesses
    Label(root, text='Your Guesses till now:', font='system 12', bg=bg, fg=fg).place(x=80, y=580)
    gtn = Text(root, width=35, height=2, font='times 10 bold', fg=bg, bg='Dark gray')  #gtn is the guesses till now box
    gtn.place(x=230, y=580)
    gtn.insert(0.0, 'Click on submit to make any guesses.')
    
    #Virtual keyboard
    button_list = list('qwertyuiopasdfghjklzxcvbnm'.upper())
    r = 410
    c = 65
    for b in button_list:
        command = lambda x=b: click(x)
        if b != "":
            Button(root, text=b, width=5, command=command).place(x=c, y=r)
        c += 50
        if c > 680-65-65 and r == 410:
            c = 93
            r += 50
        if c > 680-93-93 and r == 460:
            c = 148
            r += 50

    #Submit button
    gobut = Button(root, text="Submit", font=('system 14 bold'), command=submission, bg=bg, fg='orange')
    gobut.place(x=120, y=170)

    #exit button
    exitbut = Button(root, text="Exit", command=_quit, font=('system 14 bold'), bg=bg, fg='#fff000000')
    exitbut.place(x=0, y=580)

    head = Label(root, text="            The Hangman Game             ", font=('system 30 bold underline'), bg=bg, fg=fg)
    head.grid(columnspan=5)
    authors = Label(root, text='-By:Dhruval PB', font=('helvetica 10 bold'), bg=bg, fg=fg)
    authors.place(x=525, y=525)
    root.mainloop()

#Start menu
Button(top ,text="Play", command=link,font=('Time 20 bold'),bg='black',fg='orange').place(x=125,y=150)
Label(top, text="HANGMAN",font=('Time 20 bold'),fg='#00ff00',bg='black').place(x=100,y=0)
top.configure(bg='black')
Label(top, text="Click the button below\n to start the game",font=('Time 20 bold'),bg='black',fg='#00ff00').place(x=20,y=50)
Label(top,text='By:Dhruval PB',font=('Time 13 bold'),bg='black',fg='#00ff00').place(x=118,y=340)


def _exit():
    tkinter.messagebox.showinfo("The Hangman Game", 'Hope you liked our game!!\nHave a nice day')
    exit()
Button(top, text="Exit", command=_exit, font=('Time 14 bold'),fg='#ff0000',bg='black').place(x=140, y=250)

top.mainloop()
