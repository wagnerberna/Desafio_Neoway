from flask_restful import Resource, reqparse
from models.candidate import CandidateModel
from service.messages import *


class CandidatesController(Resource):
    def get(self):
        return {"candidates": [candidate.json() for candidate in CandidateModel.query.all()]}


class CandidateControllerRegister(Resource):
    attributes = reqparse.RequestParser()
    attributes.add_argument(
        "name",
        type=str,
        required=False,
    )
    attributes.add_argument(
        "score",
        type=float,
        required=False,
    )
    attributes.add_argument(
        "cpf",
        type=str,
        required=False,
    )
    attributes.add_argument(
        "valid_cpf",
        type=bool,
        required=False,
    )

    def post(self):
        data = CandidateControllerRegister.attributes.parse_args()
        candidate_model = CandidateModel(**data)

        cpf = data.get("cpf")
        find_cpf = CandidateModel.find_cpf(cpf)
        if find_cpf:
            return CPF_ALREDY_EXISTS, 409
        try:
            candidate_model.save_candidate()
        except:
            return SAVE_INTERNAL_ERROR, 500
        return candidate_model.json(), 201


class CandidateController(Resource):
    attributes = reqparse.RequestParser()
    attributes.add_argument(
        "name",
        type=str,
        required=True,
        help=FIELD_NOT_BLANK.format("name"),
    )
    attributes.add_argument(
        "score",
        type=float,
        required=True,
        help=FIELD_NOT_BLANK.format("score"),
    )
    attributes.add_argument(
        "cpf",
        type=str,
        required=True,
        help=FIELD_NOT_BLANK.format("cpf"),
    )
    attributes.add_argument(
        "valid_cpf",
        type=bool,
        required=True,
        help=FIELD_NOT_BLANK.format("valid_cpf"),
    )

    def get(self, candidate_id):
        candidate_model = CandidateModel.find_candidate(candidate_id)
        if candidate_model:
            return candidate_model.json(), 200
        return NOT_FOUND, 404

    def put(self, candidate_id):
        data = CandidateController.attributes.parse_args()
        candidate_model = CandidateModel.find_candidate(candidate_id)
        try:
            candidate_model.update_candidate(**data)
            return candidate_model.json(), 200
        except:
            return SAVE_INTERNAL_ERROR, 500

    def delete(self, candidate_id):
        candidate_model = CandidateModel.find_candidate(candidate_id)
        if candidate_model:
            try:
                candidate_model.delete_candidate()
                return DELETED, 200
            except:
                return DELETED_INTERNAL_ERROR, 500
        return NOT_FOUND, 404
