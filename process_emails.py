import json
from datetime import datetime, timedelta
from database import get_all_emails
from auth import get_gmail_service


def evaluate(rule, email):
    field = rule["field"]
    pred = rule["predicate"]
    val = rule["value"]

    if field == "From":
        field_val = email[1]  
    elif field == "Subject":
        field_val = email[2]  
    elif field == "Received Date/Time":
        try:
            email_date = datetime.fromisoformat(email[4])
            days = int(val)
            compare_date = datetime.now() - timedelta(days=days)

            if pred == "less than":
                return email_date > compare_date
            elif pred == "greater than":
                return email_date < compare_date
            else:
                return False
        except Exception as e:
            print(f"❌ Date parse error for email {email[0]}: {e}")
            return False
    else:
        return False

    field_val = field_val.lower()
    val = val.lower()

    if pred == "contains":
        return val in field_val
    elif pred == "does not contain":
        return val not in field_val
    elif pred == "equals":
        return val == field_val
    elif pred == "does not equal":
        return val != field_val
    return False


def apply_actions(actions, email_id, service):
    mods = {}
    if "mark_as_read" in actions:
        print(f"📩 Marking {email_id} as READ")
        mods.setdefault("removeLabelIds", []).append("UNREAD")

    if "mark_as_unread" in actions:
        print(f"📩 Marking {email_id} as UNREAD")
        mods.setdefault("addLabelIds", []).append("UNREAD")

    if mods:
        try:
            result = service.users().messages().modify(userId='me', id=email_id, body=mods).execute()
            print(f"✅ Updated {email_id} — Labels now: {result.get('labelIds', [])}")
        except Exception as e:
            print(f"❌ Failed to update {email_id}: {e}")


def process():
    print("🔄 Loading rules and fetching emails...")
    with open("rules.json") as f:
        rule_set = json.load(f)

    service = get_gmail_service()
    emails = get_all_emails()
    print(f"📥 Found {len(emails)} emails in DB.\n")

    matched_count = 0

    for email in emails:
        print(f"— Checking Email ID: {email[0]} | From: {email[1]} | Subject: {email[2]}")
        matches = [evaluate(rule, email) for rule in rule_set["rules"]]

        if (rule_set["predicate"] == "All" and all(matches)) or \
           (rule_set["predicate"] == "Any" and any(matches)):
            print(f"✅ MATCHED → Applying actions: {rule_set['actions']}")
            apply_actions(rule_set["actions"], email[0], service)
            matched_count += 1
        else:
            print("🚫 Not matched.\n")

    print(f"\n🎯 Done. {matched_count} emails matched and were updated.")


if __name__ == "__main__":
    process()
