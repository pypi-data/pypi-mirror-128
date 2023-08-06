# TeleTVG

**TeleTVG created with Telethon [Telegram apis wrapper].**
* **For using TeleTVG, you need to create your own api-id and api-hash.**
    * **Please visit:**  
        > **https://github.com/LonamiWebs/Telethon/blob/master/readthedocs/basic/signing-in.rst** 

        **for explanation.**  
* **After create id and hash, it will store in user environment encrypted.**
    * **The encryption method is using Clien-karjakak.**
        > **https://pypi.org/project/Clien-karjakak**  

### Install
```
pip install -U teletvg-karjakak
```
### Usage
**For Windows:**
```
> ttvg
```
**For MacOS X:**
```
% ttvg
```
**With script:**
```
from teletvg import main

main()
```
### Highlight
* **Schedule message.**
    * **To a user or multiple users in a group as one-to-one.**
* **Send message to a user or multiple users in a group as one-to-one.**
* **Send file to user or multiple users in a group as one-to-one.**
* **Text-expander.**
    * **Expanding a simple abbreviation to a long words.**
* **Can write markdown text.**
* **Emoji Templates.**
    * **Often used emojies can be saved and re-use.**
### Take Note:
* **Can only log-in as existing user.**
    * **No Sign-Up as New User.**
* **No multiple account users log-in.**
* **Can Request for additional module:**
    * **Need support donation :heart:**
* **For MacOS X:**
    * **~~Emoji is disabled.[tkinter issue!]~~**
    * **Emoji is Working in Python 3.10**
### Changes:
* **Some bugs fix on "GET REPLY" function.**
    * **While event-loop on going, it will not run "GET REPLY" function.**
    * **Will reassign "GET REPLY" again for next loop.**
* **Add for Help TeleTVG.pdf.**
    * **"Ctrl+F1" in Windows and "fn+F1" in MacOS X.**
* **Add protection archive.**
### TIPS
* **If user want to copy with "Ctrl-v" on Get Reply message screen, make sure on the Send Message screen is empty. [Only works in Windows]**
    * **"COPY" function only works on editable screen [Send Message screen].** 

![TeleTVG](/pics/TeleTVG.png)