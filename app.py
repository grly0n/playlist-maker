from tkinter import *
from tkinter import ttk, filedialog
from startup import verify_credentials
from spotipy import exceptions
from pathlib import Path

def center_window(tk: Tk, width: int, height: int) -> None:
    'Centers the application window in the middle of the screen and sizes the window given a height and width.'
    screen_width = tk.winfo_screenwidth()
    screen_height = tk.winfo_screenheight()
    center_x = int(screen_width/2 - width/2)
    center_y = int(screen_height/2 - height/2)
    tk.geometry(f'{width}x{height}+{center_x}+{center_y}')
    return


class App(Tk):
    def __init__(self, credentials: list[str], master=None):
        super().__init__(master)
        self.SPOTIFY = verify_credentials(credentials[0], credentials[1])
        self.CurrentLine = 0
        self.selection = tuple()
        self.editingIndex = None
        self.title("Playlist Maker")
        self.init_window()
        self.create_widgets()


    def init_window(self) -> None:
        'Initializes various window attributes'
        center_window(self, 650, 400)
        self.resizable(False, False)
        self.iconbitmap("./resources/note.ico")


    def create_widgets(self) -> None:
        'Initializes widgets inside the window'
        # Widget initialization
        # Frames
        options_frame = ttk.Frame(self)
        list_frame = ttk.Frame(self)
        # Labels
        enter_label = ttk.Label(options_frame, text="Enter Spotify link:")
        artist_label = ttk.Label(options_frame, text="Artist:")
        title_label = ttk.Label(options_frame, text="Title:")
        album_label = ttk.Label(options_frame, text="Album:")
        duration_label = ttk.Label(options_frame, text="Duration:")
        # Entries
        link_entry = ttk.Entry(options_frame)
        artist_entry = ttk.Entry(options_frame, state=DISABLED)
        title_entry = ttk.Entry(options_frame, state=DISABLED)
        album_entry = ttk.Entry(options_frame, state=DISABLED)
        duration_entry = ttk.Entry(options_frame, state=DISABLED)
        # Buttons
        edit_button = ttk.Button(options_frame, text="Edit", state=DISABLED)
        save_button = ttk.Button(options_frame, text="Save", state=DISABLED)
        delete_button = ttk.Button(options_frame, text="Delete", state=DISABLED)
        cancel_button = ttk.Button(options_frame, text="Cancel", state=DISABLED)
        export_button = ttk.Button(options_frame, text="Export", state=DISABLED)
        logout_button = ttk.Button(list_frame, text="Log out", state=ACTIVE)
        # Listbox
        xscrollbar = ttk.Scrollbar(list_frame, orient=HORIZONTAL)                
        list_box = Listbox(list_frame, width=60, height=20, selectmode=BROWSE, xscrollcommand=xscrollbar.set)
        xscrollbar.config(command=list_box.xview)


        # Widget geometry management
        # Frames
        options_frame.grid(column=0, row=0, sticky=NSEW)
        list_frame.grid(column=1, row=0, sticky=NSEW)
        # Labels
        enter_label.grid(column=0, row=0, padx=5, pady=5, stick=W)
        artist_label.grid(column=0, row=2, padx=5, sticky=E)
        title_label.grid(column=0, row=3, padx=5, sticky=E)
        album_label.grid(column=0, row=4, padx=5, sticky=E)
        duration_label.grid(column=0, row=5, padx=5, sticky=E)
        # Entries
        link_entry.grid(column=1, row=0, padx=5, pady=5, sticky=W)
        artist_entry.grid(column=1, row=2, padx=5, sticky=W)
        title_entry.grid(column=1, row=3, padx=5, sticky=W)
        album_entry.grid(column=1, row=4, padx=5, sticky=W)
        duration_entry.grid(column=1, row=5, padx=5, sticky=W)
        # Buttons
        edit_button.grid(column=0, row=1)
        delete_button.grid(column=1, row=1)
        save_button.grid(column=0, row=6)
        cancel_button.grid(column=1, row=6)
        export_button.grid(column=0, row=7)
        logout_button.grid(column=3, row=7, sticky=W)
        # Listbox
        list_box.grid(column=2, row=0, pady=5, rowspan=5, columnspan=2, sticky=NSEW)
        xscrollbar.grid(column=2, row=6, columnspan=2, sticky=NSEW)

        # Initialize data structures to pass widgets as arguments
        entries = {'artist': artist_entry, 'title': title_entry, 'album': album_entry, 'duration': duration_entry}
        buttons = {'edit': edit_button, 'delete': delete_button, 'save': save_button, 'cancel': cancel_button, 'export': export_button}

        # Bind events to widgets
        list_box.bind('<<ListboxSelect>>', lambda event=None: self.select_song(edit_button, delete_button, list_box.curselection()))
        link_entry.bind("<Return>", lambda event=None: self.enter_song(link_entry, list_box, buttons))
        edit_button.bind("<Button-1>", lambda event=None: self.edit_song(list_box, entries, buttons, list_box.curselection()))
        save_button.bind("<Button-1>", lambda event=None: self.save_edit(list_box, entries, buttons))
        cancel_button.bind("<Button-1>", lambda event=None: self.cancel_edit(entries, buttons))
        delete_button.bind("<Button-1>", lambda event=None: self.delete_song(list_box, entries, buttons))
        export_button.bind("<Button-1>", lambda event=None: self.export_list())
        logout_button.bind("<Button-1>", lambda event=None: self.logout(logout_button))


    def select_song(self, edit_button: ttk.Button, delete_button: ttk.Button, selection: tuple):
        'Upon song selection in the ListBox, edit and delete buttons are activated'
        if len(selection):
            edit_button.config(state=ACTIVE)
            delete_button.config(state=ACTIVE)
            self.selection = selection


    def enter_song(self, link_entry: ttk.Entry, list_box: Listbox, buttons: dict[str, ttk.Button]) -> None:
        'Upon entering a Spotify song link, extract information and add to ListBox'
        # Get the Spotify song link
        track_url = link_entry.get()
        link_entry.delete(0, END)
        
        # Get Spotify track information
        try:
            track_info = self.SPOTIFY.track(track_url)
        except exceptions.SpotifyException:
            print("Invalid song URL")
            return
        
        artist = track_info['album']['artists'][0]['name'].replace(" - ", "-")
        title = track_info['name'].replace(" - ", "-")
        album = track_info['album']['name'].replace(" - ", "-")
        duration = (int)(track_info['duration_ms']/1000)
        minutes = (int)(duration / 60)
        seconds = duration % 60

        # Insert formatted information into list
        list_entry = "{0} - {1} - {2} - {3}:{4:02d}".format(artist, title, album, minutes, seconds)
        list_box.insert(self.CurrentLine, list_entry)
        self.CurrentLine += 1
        if self.CurrentLine == 1: buttons['export'].config(state=ACTIVE)
        


    def edit_song(self, list_box: Listbox, entries: dict[str, ttk.Entry], buttons: dict[str, ttk.Button], selection: tuple) -> None:
        'Get information from song in list'
        self.selection = selection
        if len(selection):
            entry = list_box.get(self.selection[0])
            self.editingIndex = self.selection[0]
            words = entry.split(" - ")

            # Activate entries, save and cancel buttons
            entries['artist'].config(state=ACTIVE)
            entries['title'].config(state=ACTIVE)
            entries['album'].config(state=ACTIVE)
            entries['duration'].config(state=ACTIVE)
            buttons['save'].config(state=ACTIVE)
            buttons['cancel'].config(state=ACTIVE)

            # Clear entries from previous call to edit
            entries['artist'].delete(0, END)
            entries['title'].delete(0, END)
            entries['album'].delete(0, END)
            entries['duration'].delete(0, END)

            # Insert song information into entries to edit
            entries['artist'].insert(END, words[0].strip())
            entries['title'].insert(END, words[1].strip())
            entries['album'].insert(END, words[2].strip())
            entries['duration'].insert(END, words[3].strip())
        else:
            buttons['edit'].config(state=DISABLED)


    def save_edit(self, list_box: Listbox, entries: dict[str, ttk.Entry], buttons: dict[str, ttk.Button]) -> None:
        'Apply edited song information to entry in ListBox'
        # Get updated song information from entries
        updated_artist = entries['artist'].get().replace(" - ", "-").strip()
        updated_title = entries['title'].get().replace(" - ", "-").strip()
        updated_album = entries['album'].get().replace(" - ", "-").strip()
        updated_duration = entries['duration'].get().replace(" - ", "-").strip()
        updated_entry = "{0} - {1} - {2} - {3}".format(updated_artist, updated_title, updated_album, updated_duration)
 
        # Delete old song, insert updated song into list
        list_box.delete(self.editingIndex)
        list_box.insert(self.editingIndex, updated_entry)
        # Finish edit function
        self.cancel_edit(entries, buttons)


    def cancel_edit(self, entries: dict[str, ttk.Entry], buttons: dict[str, ttk.Button]):
        'Clear song information entries'
        # Clear entry fields
        entries['artist'].delete(0, END)
        entries['title'].delete(0, END)
        entries['album'].delete(0, END)
        entries['duration'].delete(0, END)

        # Disable entries and buttons
        entries['artist'].config(state=DISABLED)
        entries['title'].config(state=DISABLED)
        entries['album'].config(state=DISABLED)
        entries['duration'].config(state=DISABLED)
        buttons['save'].config(state=DISABLED)
        buttons['cancel'].config(state=DISABLED)
        buttons['edit'].config(state=DISABLED)
        buttons['delete'].config(state=DISABLED)

        # Clear selection
        self.selection = tuple()


    def delete_song(self, list_box: Listbox, entries: dict[str, ttk.Entry], buttons: dict[str, ttk.Button]):
        'Remove the selected song from the ListBox'
        if len(self.selection):
            list_box.delete(self.selection[0])
            self.CurrentLine -= 1
            self.cancel_edit(entries, buttons)
            if self.CurrentLine == 0: buttons['export'].config(state=DISABLED)
        # If no song is selected, disable the delete button
        else:
            buttons['delete'].config(state=DISABLED)


    def export_list(self):
        directory = filedialog.askdirectory()
        print("Exporting list to ", directory)


    def logout(self, button: ttk.Button):
        Path.unlink(".login")
        button.after(1, self.destroy)