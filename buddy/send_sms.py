from twilio.rest import Client

account_sid = 'AC8b19f343b4618e4352bc8d9141b5dfc3'
auth_token = '6061cb4f8e13f535305f57442d388d8e'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Testing Again.",
                     from_='+14153013594',
                     to='+14156230074'
                 )

print(message.sid)