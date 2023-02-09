import imaplib
import email
from twilio.rest import Client

mail = imaplib.IMAP4_SSL("imap.terpmail.umd.edu")
mail.login("your_email",  "your_email_password")
mail.select("inbox")

result, data = mail.search(None, "(From 'umterps@umd.edu' SUBJECT 'Student Ticket')")
if data[0]:
    
    # Retrieve recent email
    latest_email_id = data[0].split()[-1]
    result, email_data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = email_data[0][1].decode("utf-8")
    email_message = email.message_from_string(raw_email)
    game_details = email_message.get_payload()
    
    # Send text message to your phone
    account_sid = "your_twilio_account_sid"
    auth_token = "your_twilio_auth_token"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        # Make sure if you are living in the US, you include the '+1' before your phone number
        to="your_phone_number", 
        from_="your_twilio_phone_number", 
        body=game_details
    )
    print("Text message sent successfully!")
else:
    print("No email found")

# Log out from email account
mail.logout()