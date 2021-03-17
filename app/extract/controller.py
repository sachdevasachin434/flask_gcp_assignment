"""
    Endpoint controller layer of the project
"""
from flask import request, Response, jsonify
from flask_restx import Resource, Namespace
from marshmallow import ValidationError
from .service.service import GetBookData
from .validators import UserSchema

API = Namespace("Extract", description="Extract API")


@API.route("/books_info")
class GetLongitudeLattitude(Resource):
    """
    Class handling HTTP requests to endpoint /books_info
    """

    @classmethod
    def get(cls):
        """Flask Post Method

        Returns:
            json: Returns result containing input and output.
        """
        try:
            UserSchema().load(request.args)
        except ValidationError as err:
            return {"error_message": str(err)}, 400
        q_value = request.args.get("q_value")
        output = GetBookData.fetch_json(q_value)
        return jsonify(**output)