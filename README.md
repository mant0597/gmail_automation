# 📬 Gmail Automation Script

This Python project connects to your Gmail account using the Gmail API, fetches recent emails, stores them in a local SQLite database, and applies user-defined rules to automatically perform actions like marking emails as **read** or **unread**.

---

## ✨ Features

- 🔐 Secure Gmail OAuth2 authentication
- 📥 Fetch recent emails using the Gmail REST API
- 🗃️ Store email metadata in SQLite
- ⚙️ Define rule conditions in JSON (`rules.json`)
- ✅ Supported actions:
  - Mark email as **read**
  - Mark email as **unread**
- 🧩 Supports field-based matching on sender, subject, and received date

---

## 🧰 Technologies Used

- Python 3.7+
- Gmail REST API
- SQLite3
- Google API Python Client

---

## 🔧 Setup Instructions

### 1. 📦 Clone the Repository & Install Dependencies

git clone https://github.com/mant0597/gmail_automation.git
cd gmail_automation
pip install -r requirements.txt

2. 🔐 Enable Gmail API & Set Up OAuth
This is only required once to allow access to your Gmail account.

Go to Google Cloud Console

Create a new project

Navigate to APIs & Services → Library

Search for Gmail API and click Enable

Navigate to APIs & Services → OAuth consent screen

Choose External

Add your email as a test user

Navigate to APIs & Services → Credentials

Click Create Credentials → OAuth client ID

Application type: Desktop App

Click Create and Download JSON

Rename the downloaded file to credentials.json and place it in the project folder


1. 🔄 Fetch Emails and Store in SQLite

python fetch_emails.py
Opens a browser for OAuth2 Gmail login

Fetches 50 recent emails

Saves metadata to emails.db

2. ✍️ Define Rules in rules.json
📌 Example:
json

{
  "predicate": "All",
  "rules": [
    {
      "field": "From",
      "predicate": "contains",
      "value": "manthaork97@gmail.com"
    },
    {
      "field": "Received Date/Time",
      "predicate": "greater than",
      "value": "120"
    }
  ],
  "actions": ["mark_as_read"]
}
✅ Supported Fields:
"From" (sender)

"Subject"

"Received Date/Time"

✅ Supported Predicates:
String-based: contains, equals, does not contain, does not equal

Date-based (in days): less than, greater than

✅ Supported Actions:
mark_as_read

mark_as_unread

3. ⚙️ Process Emails and Apply Rules

python process_emails.py
This script:

Loads all emails from the DB

Applies rules from rules.json

Marks matched emails as read/unread using the Gmail API

