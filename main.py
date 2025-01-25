import app
import startup
import os
import time

def read_credentials() -> list[str]:
    if not os.path.isfile('.login'):
        return []
    with open('.login', 'r') as login_file:
        for line in login_file:
            return line.split(" ")

if __name__ == "__main__":
    showLogin = False
    if not os.path.isfile('.cache'):
        showLogin = True
    else: 
        with open('.cache', 'r') as cache_file:
            for line in cache_file:
                epoch_time = int(time.time())
                expires = int(line.split(":")[4].split("}")[0].strip())
                if expires <= epoch_time:
                    showLogin = True

    print("Running application...")
    if showLogin:
        startupWindow = startup.Startup()
        startupWindow.mainloop() 

        # If credentials were invalid, exit without launching application
        if startup.VALID_CRED == 0:
            quit()

    # Read previously stored credentials
    credentials = read_credentials()
            
    myApp = app.App(credentials)
    myApp.mainloop()
    print("Application terminated successfully")