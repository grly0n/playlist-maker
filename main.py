import app
import startup
import os
import time

def read_credentials() -> list[str]:
    'Searches for credentials from a previous login'
    if not os.path.isfile('.login'):
        return []
    with open('.login', 'r') as login_file:
        for line in login_file:
            return line.split(" ")

if __name__ == "__main__":

    print("Running application...")


    # Read previously stored credentials
    credentials = read_credentials()
    showLogin = bool(not len(credentials))

    # Show login screen if credentials are needed
    if showLogin:
        startupWindow = startup.Startup()
        startupWindow.mainloop() 

        # If credentials were invalid, exit without launching application
        if startup.VALID_CRED == 0:
            quit()
            
    # Launch app with credentials
    myApp = app.App(credentials)
    myApp.mainloop()
    
    print("Application terminated successfully")