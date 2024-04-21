# ShellBack
-------------------------------------------------------------------

 * This Python script is designed to provide remote access to a target machine.
 * It allows for various functionalities such as executing commands, taking screenshots, streaming the screen, uploading and downloading files, and more.
   Usage
## requirements & Compile Python To EXE
-------------------------------------------------------------------------------- 
   * Install all Packages from requirements.txt in Windows machine 
   ```
    pip install -r requirements.txt
   ```
  * Use pyinstaller in compile the CallBack.py to CallBack.exe
  ```
  pyinstaller -w -F CallBack.py
  ```
## Setting up the Listener
------------------------------------------------------------------------------
   * Before using the script, you need to set up a listener on your machine.
   * Use stage.py as the listener and set the port number in CallBack.py to the same port number in stage.py to establish the connection.
   * you can use  netcat listener tool on the specified IP address and port (LHOST and LPORT variables).

## Running the Script
--------------------------------------------------------------------------------
  * Ensure you have Python 3 installed on the target machine.
  * Modify the LHOST and LPORT variables in the script to match the IP address and port of your listener.

## Interacting with the Target
------------------------------------------------------------------------------------
  * Once the script is running on the target machine, you can interact with it by connecting to the listener from your machine.
  * Use commands like screenshot, stream, cd, quit, etc., to perform various actions on the target machine.
    ### *  Additional Notes
    ---------------------------------------------------------------------------------------------
       *  The script provides basic error handling, but use it at your own risk.
       *  Make sure you have appropriate permissions before running the script on any machine.

## Functionality
----------------------------------------------------------------------------------
  * Command Execution: You can execute shell commands on the target machine.
  *  File Operations: Upload and download files to/from the target machine.
  *  Screen Capture: Take screenshots of the target machine's screen.
  *  Screen Streaming: Stream the target machine's screen to the listener.
  *  Error Handling: Basic error handling is implemented to handle certain scenarios.


## Disclaimer
---------------------------------------------------------------------------------------------------
  * This script is for educational purposes only. Do not use it on any system without proper authorization.
  * The author holds no responsibility for any misuse of this script.
