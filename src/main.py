import app
import startup
import os
import time

from sys import platform

def read_credentials() -> list[str]:
    'Searches for credentials from a previous login'
    if not os.path.isfile('.login'):
        return []
    with open('.login', 'r') as login_file:
        for line in login_file:
            return line.split(" ")

if __name__ == "__main__":

    print(f"Running application on {platform}...")


    # Read previously stored credentials
    credentials = read_credentials()

    # Show login screen if credentials are needed
    if not len(credentials):
        startupWindow = startup.Startup()
        startupWindow.mainloop() 

        # If credentials were invalid, exit without launching application
        if not startup.VALID_CRED:
            print("Exiting application (invalid credentials)")
            exit()

        credentials = read_credentials()
    
    # Launch app with credentials
    myApp = app.App(credentials)
    myApp.mainloop()
    
    print("Application terminated successfully")