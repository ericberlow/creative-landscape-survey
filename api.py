from flask import Flask, request, Response
from flask_restful import Api, Resource, reqparse
from process_respondents import process_single_respondent
import json
app = Flask(__name__)
api = Api(app)


class Questionnaire(Resource):
  def post(self):
        respondent = request.json
        result = process_single_respondent(respondent)
        return Response(json.dumps(result), mimetype='application/json')


api.add_resource(Questionnaire, "/questionnaire", "/questionnaire/")

if __name__ == '__main__':
    app.run(debug=True)