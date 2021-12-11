from random import choice
from hangman_words import word_list
from tkinter import ttk, Tk, PhotoImage, RAISED, Label, Entry, Button, messagebox
from string import ascii_uppercase


class HangMan:
    # Window Initialisation
    root = Tk()
    root.title("Hang Man Game")
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(f"{width // 2}x{height // 2}+100+100")

    # Load Logo Imange
    logo_image = PhotoImage(file='./Art/logo.png')

    # Load Hanging Images in List 0 Fully Hanged 6 Starting
    hangman_image = [PhotoImage(file=f'./Art/Hang{i}.png') for i in range(0, 7, 1)]

    def __init__(self):

        # Initialise Variables
        self.chosen_word = ""
        self.lives = 0
        self.not_used_letters = []
        self.display_word_var = ""

        # Tkinter Variables
        self.guess_word_Entry = None

        # Validate The entry is a Letter Callback Function
        # Check single Letter, Valid Alphabet
        def validate_entry(entry):
            entry = entry.upper()
            if len(entry) > 1:
                return False
            elif entry not in ascii_uppercase:
                return False
            else:
                return True

        # Entry Field Validation Callback
        self.reg = self.root.register(validate_entry)

        # Random Word Frame
        self.random_word_Frame = ttk.Frame(self.root, relief=RAISED, padding=5)
        self.random_word_Frame.place(x=0, y=0, width=self.width // 4, height=self.height // 4, relx=0.005, rely=0.005)

        # Guess Word Frame
        self.guess_word_Frame = ttk.Frame(self.root, relief=RAISED, padding=5)
        self.guess_word_Frame.place(x=0, y=self.height // 4, width=self.width // 4, height=self.height // 4, relx=0.005,
                                    rely=0.005)

        # Image Word Frame
        self.image_Frame = ttk.Frame(self.root, relief=RAISED, padding=5)
        self.image_Frame.place(x=self.width // 4, y=0, width=self.width // 4, height=self.height // 2, relx=0.005,
                               rely=0.005)

        # Set Column Size for Unused columns/Rows
        self.random_word_Frame.grid_columnconfigure(0, minsize=30)
        self.random_word_Frame.grid_rowconfigure(0, minsize=70)
        # self.image_Frame.grid_rowconfigure(0, minsize=150)

        # Random Word Display as '_'
        self.random_word_Label = Label(self.random_word_Frame, text=self.display_word_var, font=('Arial', 25))
        self.random_word_Label.grid(row=1, column=1)

        # Random Word Guess Entry
        self.guess_word_Label = Label(self.guess_word_Frame, text="Enter Your Guess", font=('Arial', 15))
        self.guess_word_Label.pack(fill='x')

        self.guess_word_Entry = Entry(self.guess_word_Frame, font=('Arial', 15), validate='key',
                                      validatecommand=(self.reg, '%P'))
        self.guess_word_Entry.pack(fill='x')
        self.guess_word_Entry.focus()

        self.guess_word_Button = Button(self.guess_word_Frame, text="Check the Guess", command=self.check_the_guess)
        self.guess_word_Button.pack()

        # Image Showing
        self.photo_label = Label(self.image_Frame, image=self.logo_image)
        self.photo_label.grid(row=0, column=0)

        self.play_game()

    def check_the_guess(self):

        # String to List which is Displaying Guessing Process
        display_word_list = self.display_word_var.split(" ")

        # Guessed Letter Saved to a Shorter Named Variable
        guessed = self.guess_word_Entry.get().upper()

        # Check If Click on Button without Entering any Letter
        if guessed != "":

            # Clear Entry Field
            self.guess_word_Entry.delete(0, 'end')

            # Check The Letter Earlier Used or Not
            if guessed not in self.not_used_letters:
                messagebox.showerror("Repeated Guess", "You already Tried This Letter")
            else:

                # Remove Current Guessed Letter From Not Used Letters List
                self.not_used_letters.remove(guessed)

                # Check The Letter In Computer Selected Word
                if guessed in self.chosen_word:

                    # Using Loop Find The letter is Repeating in Computer Selected Word
                    for index in range(len(self.chosen_word)):

                        # Get The Index of the Letter in Computer Selected Word
                        if guessed == self.chosen_word[index]:

                            # Update The Guessing Indicator List
                            display_word_list[index] = guessed

                    # Update the String From List
                    self.display_word_var = " ".join(display_word_list)

                    # Show In Progress Label
                    self.random_word_Label.config(text=self.display_word_var)

                    # Check All Letters Guessed or not
                    if "_" not in display_word_list:

                        # All Letters Guessed Ask to Play Again & Show Score
                        play_again = messagebox.askyesno("Success", f"You Won The Game\n\
Remaining Life {self.lives}\nDo you Want to Play Again?")
                        if play_again:
                            self.play_game()
                        else:

                            # Exit Game
                            self.root.quit()
                else:

                    # Predicted Letter Not in the Word Lost 1 Life
                    self.lives -= 1
                    if self.lives > 0:

                        # Change the Hanging Image By The Level
                        self.photo_label.config(image=self.hangman_image[self.lives])
                    else:

                        # Failed Show Last Hanging Image
                        self.photo_label.config(image=self.hangman_image[0])

                        # Word Prediction Failed Ask to Play Again
                        play_again = messagebox.askyesno("Failed",
                                                         f"You Word Guessing Failed and the Man Hanged\n\
Do you want to Play again?")
                        if play_again:
                            self.play_game()
                        else:

                            # Exit Game
                            self.root.quit()
        else:
            messagebox.showerror("Blank Error", "Please Enter the Guessed Letter")

    def play_game(self):

        # Randomly Select a Word from Word List
        self.chosen_word = choice(word_list).upper()

        # Set Life as 7 (available Life is 6)
        self.lives = 7

        # All Letters Uppercase Letters In List
        # Used to Detect Repeated Usage of Letters
        self.not_used_letters = [i for i in ascii_uppercase]

        # Data To display Word Under Guessing
        self.display_word_var = '_ ' * len(self.chosen_word)

        # Display '_' As the Progress for the Word to be Predicted
        self.random_word_Label.config(text=self.display_word_var)

        # First Image is Game Logo
        self.photo_label.config(image=self.logo_image)

    # Run Tkinter Window
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    hangman = HangMan()
    hangman.run()
