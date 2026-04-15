# gmail2newsletter

# AI Disclaimer
The AI Claude was used for only some very minor debugging when it came to messing with my own python version and it was spitting out an error and what it did for that was show me what built in python libraries to include that bypasses the warnings at the very top of the code. It also was not used to generate any of the code.


# Resources/Tools Used.
Used for finding color hex codes and also finding what colors work well together as it has that on its website. - https://colorcodefinder.com/colors

This was used as a pretty big baseline in learning how to even begin to use Google’s gmail API with python. -https://www.geeksforgeeks.org/python/how-to-read-emails-from-gmail-using-gmail-api-in-python/

Used for my HTML work - https://www.geeksforgeeks.org/html/html-tutorial/

Used for learning how to have python use HTML for using it to output the newsletter in users email - https://www.geeksforgeeks.org/python/creating-and-viewing-html-files-with-python/

Google’s Cloud Console which is what I used - https://console.cloud.google.com/

Google’s Gmail API Quickstart Guide - https://mailmeteor.com/blog/gmail-api

This tutorial of MIME being used that I used - https://pytutorial.com/how-to-send-an-email-with-attachment-in-python/


# Libraries

These are built into Python as I had to use them since python was giving me an issue on version control (this was the only recommendation that I had to ask Claude on) and this does not change anything when using it on other machines its just how I got mine to stop giving me version errors
warnings
os
sys

Google API Libraries
googleapiclient.discovery
google_auth_oauthlib.flow
google.auth.transport.requests

The Email Building Libraries
email.mime.multipart
email.mime.text

Utility Libraries
pickle
os.path
base64
email

Parsing Library
Bs4 (BeautifulSoup)


# What does the Program do?

When it comes to what the program looks for when scraping through your email I have set query words that it looks for which could easily be changed especially if I were to make a front end for this I could have it have a menu where the user could easily add and remove key words or phrases. Another feature that is available when scraping through the user's email is the option to look for only unread emails with the set keywords or even to look for emails from specific email addresses.

# Constraints and potential future improvements.

The reason for only being able to only use Gmail accounts was due to the constraints around using Outlook as that was my first option. With Outlook my college does not allow students to know our Azure ID to be able to sign into Outlook without having to jump through the login hoops. So for me personally other than my college email I pretty much strictly use Gmail accounts so I looked into their APIs and found that it was much easier and way more documented than Outlooks. Another solution that I did find with using Outlook emails was to just have the script actually interact with the Outlook program on windows as there are ways of doing that but I would rather this program be cross platform compatible (as I myself mainly use Mac OS) than it be just limited to one operating system. A potential improvement that I have researched is being able to use any email with this software by setting up a proxy gmail that would be like a duplicate of your own email and would allow it to scrape the data and then when it would send it to that email it would also send it to the original email.
