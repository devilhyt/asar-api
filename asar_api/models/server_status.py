from ..extensions import db


class ServerStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    training_status = db.Column(db.Boolean, nullable=False)
    training_result = db.Column(db.Integer, nullable=False)
    training_time = db.Column(db.DateTime, nullable=True)
    training_project = db.Column(db.String, nullable=True)
    training_message = db.Column(db.String, nullable=True)

    @classmethod
    def init(cls):
        if ServerStatus.query.first() is None:
            status = ServerStatus(training_status=False,
                                  training_result=-1, 
                                  training_project=None,
                                  training_message=None)
            db.session.add(status)
            db.session.commit()
        else:
            status = ServerStatus.query.first()
            status.training_status = False
            status.training_message = None
            db.session.commit()
