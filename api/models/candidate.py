from sql_alchemy import db


class CandidateModel(db.Model):
    __tablename__ = "candidates"

    candidate_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    score = db.Column(db.Float(precision=2))
    cpf = db.Column(db.String(11))
    valid_cpf = db.Column(db.Boolean)

    def __init__(self, name, score, cpf, valid_cpf):
        self.name = name
        self.score = score
        self.cpf = cpf
        self.valid_cpf = valid_cpf

    def json(self):
        return {
            "candidate_id": self.candidate_id,
            "name": self.name,
            "score": self.score,
            "cpf": self.cpf,
            "valid_cpf": self.valid_cpf,
        }

    @classmethod
    def find_candidate(cls, candidate_id):
        candidate = cls.query.filter_by(candidate_id=candidate_id).first()
        if candidate:
            return candidate
        return None

    @classmethod
    def find_cpf(cls, cpf):
        candidate = cls.query.filter_by(cpf=cpf).first()
        if candidate:
            return True
        return False

    def save_candidate(self):
        db.session.add(self)
        db.session.commit()

    def delete_candidate(self):
        db.session.delete(self)
        db.session.commit()

    def update_candidate(self, name, score, cpf, valid_cpf):
        self.name = name
        self.score = score
        self.cpf = cpf
        self.valid_cpf = valid_cpf
        db.session.commit()
