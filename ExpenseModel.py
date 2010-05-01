from google.appengine.ext import db

class ExpenseModel(db.Model):
    name = db.StringProperty(required=True)
    type = db.StringProperty(required=True, choices=set(["credit", "debit"]))
    date = db.DateTimeProperty(required=True)
    owner = db.UserProperty(required=True)
