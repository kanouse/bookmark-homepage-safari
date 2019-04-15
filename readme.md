[Python 3]

# What is this? 
This repo contains a python script that reads Safari browsing history to create a home page of links to site according to frequency and quality. Safari history is contained in a sqlite file. The script includes various SQL which separates links from amazon.com into a separate section because that's my work domain and I'm there a lot. History queries can be updated to use differnt domains.

To execute .command files, give execute privilages:  
`chmod u+x /[%path%]/rebuild-bookmarks.command`

To set page as home page, double click the html file output `homepage.html'. Then, go to Safari > Preferences, then click General. Under Homepage, click "Set to Current Page"

# Mojave and SIP (System Integrity Protection)
You will not be able to access the contents of `~/Library/Safari` 
without granting Full Disk Access to Terminal.app or whichever application you are using
to launch the script. Here's how to do that: https://apple.stackexchange.com/questions/341959/how-do-programs-access-library-mail-under-osx-10-14-mojave/341967#341967
 

# How do you automate?

Keyboard Maestro (http://www.keyboardmaestro.com/main/) is great for this. Two options might be: 
* Run the script when Safari deactivates. (This happens often for me and didn't feel right to do every time.)
* Run the script every couple of hours when logged in. (This is what I did.)
* 