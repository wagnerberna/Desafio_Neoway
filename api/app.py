from flask import Flask
from flask_restful import Api
from controller.candidate import Candidates, Candidate, CandidateRegister

app = Flask(__name__)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)


@app.before_first_request
def create_db():
    db.create_all()


api.add_resource(Candidates, "/candidates")
api.add_resource(Candidate, "/candidate/<string:candidate_id>")
api.add_resource(CandidateRegister, "/register")

if __name__ == "__main__":
    from sql_alchemy import db

    db.init_app(app)
    app.run(debug=True)
