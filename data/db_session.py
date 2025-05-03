from data.models import db

def create_session():
    return db.session
