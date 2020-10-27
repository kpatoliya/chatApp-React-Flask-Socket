from server import db


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120))
    text = db.Column(db.Text)
    email = db.Column(db.Text)
    profilePic = db.Column(db.Text)

    def __init__(self, user_name, text, email, profilePic):
        self.user_name = user_name
        self.text = text
        self.email = email
        self.profilePic = profilePic

    def __repr__(self):
        return str({
            'userId': self.user_name,
            'body': self.text,
            'email': self.email,
            'profilePic': self.profilePic
        })
