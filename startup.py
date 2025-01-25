from tkinter import *
from tkinter import ttk
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


VALID_CRED = FALSE

def verify_credentials(client_id: str, client_secret: str) -> spotipy.client:
    global VALID_CRED
    SPOTIFY = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))
    try:
        SPOTIFY.track('https://open.spotify.com/track/3mwvKOyMmG77zZRunnxp9E?si=8275ce0fb7604260')
        VALID_CRED = True
    except ValueError:
        VALID_CRED = False
    return SPOTIFY


def store_credentials(client_id: str, client_secret: str) -> None:
    with open('.login', 'w') as login_file:
        login_file.write(f'{client_id} {client_secret}')


def center_window(tk: Tk, width: int, height: int) -> None:
    'Centers the application window in the middle of the screen and sizes the window given a height and width.'
    screen_width = tk.winfo_screenwidth()
    screen_height = tk.winfo_screenheight()
    center_x = int(screen_width/2 - width/2)
    center_y = int(screen_height/2 - height/2)
    tk.geometry(f'{width}x{height}+{center_x}+{center_y}')
    return

# Popup window (upon invalid credentials)
class Popup(Tk):
    def __init__(self, master=None):
        super().__init__(master)


# Startup window
class Startup(Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Playlist Maker")
        self.loggedIn = IntVar()
        global VALID_CRED
        self.init_window()
        self.create_widgets()


    def init_window(self):
        center_window(self, 300, 150)
        self.resizable(False, False)
        self.iconbitmap("./resources/note.ico")


    def create_widgets(self):
        # Frame
        frame = ttk.Frame(self)
        # Buttons
        enter_button = ttk.Button(frame, text="Enter")
        check_button = ttk.Checkbutton(frame, text="Log out after use", variable=self.loggedIn, onvalue=1, offvalue=0, command=self.on_log_out)
        # Entries
        client_id_entry = ttk.Entry(frame)
        client_secret_entry = ttk.Entry(frame)
        # Labels
        welcome_label = ttk.Label(frame, text="Welcome to Playlist Maker!")
        client_id_label = ttk.Label(frame, text="Enter Client ID:")
        client_secret_label = ttk.Label(frame, text="Enter Client Secret:")

        # Geometry management
        frame.grid(column=0, row=0, sticky=NSEW)
        welcome_label.grid(column=0, row=0)
        client_id_label.grid(column=0, row=1)
        client_secret_label.grid(column=0, row=2)
        client_id_entry.grid(column=1, row=1)
        client_secret_entry.grid(column=1, row=2)
        enter_button.grid(column=0, row=3)
        check_button.grid(column=1, row=3)

        # Action binding
        enter_button.bind("<Button-1>", lambda event=None: self.enter_info(enter_button, client_id_entry, client_secret_entry))

    def enter_info(self, enter_button: ttk.Button, client_id_entry: ttk.Entry, client_secret_entry: ttk.Entry):
        client_id = client_id_entry.get()
        client_secret = client_secret_entry.get()
        try:
            verify_credentials(client_id, client_secret)
            store_credentials(client_id, client_secret)
        except spotipy.oauth2.SpotifyOauthError:
            client_id_entry.delete(0, END)
            client_secret_entry.delete(0, END)

        if VALID_CRED:
            enter_button.after(1, self.destroy)


    def on_log_out(self):
        if self.loggedIn.get() == 1:
            print("Will log out")
        else:
            print("Will not log out")


