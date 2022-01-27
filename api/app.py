from flask import Flask
from flask_restful import Api
from controller.candidate import CandidatesController, CandidateController, CandidateControllerRegister

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)


@app.before_first_request
def create_db():
    db.create_all()


api.add_resource(CandidatesController, "/candidates")
api.add_resource(CandidateController, "/candidate/<string:candidate_id>")
api.add_resource(CandidateControllerRegister, "/register")

if __name__ == "__main__":
    from sql_alchemy import db

    db.init_app(app)
    app.run(debug=True)
