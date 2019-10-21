from app.extensions import db


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text())
    name = db.Column(db.String(64))
    actor = db.Column(db.Text())
    up_time = db.Column(db.DateTime())
    score = db.Column(db.Float())

    def __repr__(self):
        return '<User %r>' % self.name