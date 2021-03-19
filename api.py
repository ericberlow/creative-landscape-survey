from flask import Flask, request, Response
from flask_restful import Api, Resource, reqparse
import process_respondents as pr
app = Flask(__name__)
api = Api(app)


class Habits(Resource):
  def post(self, id):
        params = request.json
        result = pr.process_respondent('api_response')
        return Response(result, mimetype='application/json')


api.add_resource(Habits, "/habits", "/habits/", "/habits/<string:id>")

if __name__ == '__main__':
    app.run(debug=True)