
# from mailbox import Message
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '58efb22df382f7'
app.config['MAIL_PASSWORD'] = 'b90b70da77ca40'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

@app.route("/")
def index():
  msg = Message('Hello from the other side!', sender =   'mpt.duang.dg@gmail.com', recipients = ['tienduangmaiphan1998@gmail.com'])
  msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
  mail.send(msg)
  return "Message sent!"

if __name__ == '__main__':
   app.run(debug = True)