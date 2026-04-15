# Hides the version warnings I personally got
import warnings
import os
os.environ['PYTHONWARNINGS'] = 'ignore'
warnings.filterwarnings("ignore")

import sys
if not sys.warnoptions:
    warnings.simplefilter("ignore")

# connects to gmail API
from googleapiclient.discovery import build
# this is used to handle the Google login in the browser
from google_auth_oauthlib.flow import InstalledAppFlow
# this keeps the users login token refreshed so they dont have to sign in everytime to generate the newsletter
from google.auth.transport.requests import Request

# this is the library used to build the newsletters structure and body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# saves and loads the Google login token
import pickle
# checks if the token.pickle file exists
import os.path
# used to decode the gmail content
import base64
# built in email handler
import email
# BeautifulSoup is used to parse the HTML content inside the emails
from bs4 import BeautifulSoup

# permissions we are asking Google for
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

# this is the function used to search through the emails in the Gmail account based on the queries added
def getEmails(service):
    queries = [
        "invoice OR invoices",                      # Emails with "invoice" or "invoices" anywhere
        "plan OR idea",                             # Emails with "plan" or "idea" anywhere
        "opportunity OR opportunities",             # Emails with "opportunity" anywhere
        "meeting OR meetings",                      # Emails with "meeting" or "meetings" anywhere
        # "from:example@example.com",               # Can include any emails from a specific email
        # "from:example@example.com is:unread",     # Can only include speific email if unread
    ]

    # combines all the queries into one Gmail search string
    search_query = " OR ".join(f"({q})" for q in queries)
    print(f"Running search: {search_query}")

    # sends the search to Gmail and gets back a list of matching emails
    result = service.users().messages().list(maxResults=6, userId='me', q=search_query).execute()
    messages = result.get('messages')

    # stops if no emails match the search
    if not messages:
        print("No emails found matching your search.")
        return []

    collected = []

    # loops through each email and pulls out the subject, sender, and body
    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        try:
            payload = txt['payload']
            headers = payload['headers']

            subject = "No Subject"
            sender = "Unknown Sender"

            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']

            parts = payload.get('parts')[0]
            data = parts['body']['data']
            data = data.replace("-", "+").replace("_", "/")
            decoded_data = base64.b64decode(data)

            soup = BeautifulSoup(decoded_data, "lxml")
            body = soup.get_text(separator=' ', strip=True)[:500]  # only the first 500 chars of body just so the newsletter isnt crazy long

            collected.append({
                "subject": subject,
                "sender": sender,
                "body": body
            })

        except:
            pass

    return collected

# function that builds the HTML that makes up the newsletter
def buildNewsletter(emails):
    html = """
    <html>
    <body style="font-family: Courier New, sans-serif; max-width: 600px; margin: auto; padding: 20px;">
        <div style="text-align: center;">
            <h1 style="background-color: #87ae73; color: white; padding: 15px; border-radius: 8px;">
                Your Email Newsletter!
            </h1>
        </div>
    """
    # loops through each email and makes its own littler card using border radius in the newsletter
    for i, em in enumerate(emails, 1):
        html += f"""
        <div style= "margin-bottom: 30px; padding: 15px; border: 1px solid #ddd; border-radius: 8px;">
            <h3 style="color: #9a73ae;">#{i} — {em['subject']}</h3>
            <p><strong>From:</strong> {em['sender']}</p>
            <p style="color: #333;">{em['body']}...</p>
        </div>
        """

    html += """
        </p>
    </body>
    </html>
    """

    return html

# this function sends the finished newsletter to the users email address
def sendNewsletter(service, to_email, html_content):
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Your Email Newsletter!'
    message['From'] = to_email
    message['To'] = to_email

    mime_html = MIMEText(html_content, 'html')
    message.attach(mime_html)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    send_message = service.users().messages().send(userId='me', body={'raw': raw}).execute()
    print(f"Newsletter sent! Message ID: {send_message['id']}")

# this is the main function that runs everything in order
def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # gets the email address of the account that is signed in and outputs to the command line
    profile = service.users().getProfile(userId='me').execute()
    user_email = profile['emailAddress']
    print(f"Logged in as: {user_email}")

    # this runs the three main steps which is to fetch the emails, build the newsletter, and final send it to the users email
    # and if it does not find any emails in the fetch phase it just outputs "No emails to send in newsletter"
    emails = getEmails(service)
    if emails:
        newsletter = buildNewsletter(emails)
        sendNewsletter(service, user_email, newsletter)
    else:
        print("No emails to send in newsletter.")

main()