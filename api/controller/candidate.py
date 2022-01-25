from flask_restful import Resource, reqparse
from models.candidate import CandidateModel


class Candidates(Resource):
    def get(self):
        return {"candidates": [candidate.json() for candidate in CandidateModel.query.all()]}


class CandidateRegister(Resource):
    attributes = reqparse.RequestParser()
    attributes.add_argument(
        "name",
        type=str,
    )
    attributes.add_argument(
        "score",
        type=float,
    )
    attributes.add_argument(
        "cpf",
        type=str,
    )
    attributes.add_argument(
        "valid_cpf",
        type=bool,
    )

    def post(self):
        # if CandidateModel.find_candidate(candidate_id):
        #     return {"message": f"candidate ID: {candidate_id} alredy exists"}, 400
        data = Candidate.attributes.parse_args()
        candidate_model = CandidateModel(**data)
        try:
            candidate_model.save_candidate()
        except:
            return {"message": "An interna erro ocurred trying to save candidate."}, 500
        return candidate_model.json()


class Candidate(Resource):
    attributes = reqparse.RequestParser()
    attributes.add_argument(
        "name",
        type=str,
        required=True,
        help="The field 'name' cannot be left blank.",
    )
    attributes.add_argument(
        "score",
        type=float,
        required=True,
        help="the field 'score' cannot bel left blank",
    )
    attributes.add_argument(
        "cpf",
        type=str,
        required=True,
        help="The field 'CPF' cannot be left blank.",
    )
    attributes.add_argument(
        "valid_cpf",
        type=bool,
        required=True,
        help="The field 'valid CPF' cannot be left blank.",
    )

    def get(self, candidate_id):
        candidate_model = CandidateModel.find_candidate(candidate_id)
        if candidate_model:
            return candidate_model.json(), 200
        return {"message": "candidate not found."}, 404

    def put(self, candidate_id):
        data = Candidate.attributes.parse_args()
        candidate_model = CandidateModel.find_candidate(candidate_id)
        try:
            candidate_model.update_candidate(**data)
            return candidate_model.json(), 200
        except:
            return {"message": "An interna erro ocurred trying to save candidate."}, 500

    def delete(self, candidate_id):
        candidate_model = CandidateModel.find_candidate(candidate_id)
        if candidate_model:
            try:
                candidate_model.delete_candidate()
                return {"message": "candidate deleted."}
            except:
                return {"message": "An interna erro ocurred trying to delete candidate."}, 500
        return {"message": "candidate not found."}, 404
