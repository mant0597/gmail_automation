from auth import get_gmail_service
from database import insert_email, init_db
import base64
import email
from datetime import datetime

def parse_message(msg):
    headers = msg['payload'].get('headers', [])
    subject = sender = ""
    for header in headers:
        if header['name'] == 'From':
            sender = header['value']
        if header['name'] == 'Subject':
            subject = header['value']
    snippet = msg.get('snippet', '')
    ts = int(msg['internalDate']) / 1000
    received_at = datetime.fromtimestamp(ts).isoformat()
    return {
        'id': msg['id'],
        'sender': sender,
        'subject': subject,
        'snippet': snippet,
        'received_at': received_at
    }

def fetch_and_store():
    init_db()
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', maxResults=20).execute()
    messages = results.get('messages', [])
    
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        parsed = parse_message(msg)
        insert_email(parsed)

if __name__ == '__main__':
    fetch_and_store()
