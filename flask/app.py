#!usr/bin/env python3.8
import json
from symbol import parameters

from flask import Flask
from flask_restful import Api, Resource, reqparse

from app_helper import db_connect, json_converter, date_today_s

app = Flask(__name__)
api = Api(app)


class Scholarships(Resource):
    """Class for /scholarships route.

    Args:
        Resource (obj): Resource from the request

    """

    def get(self):
        """Get from scholarships.

        Returns:
            json: Data for all scholarships
        """
        db, cursor = db_connect()
        cursor.execute('''  SELECT * FROM Scholarship
                            INNER JOIN Reqtag R ON Scholarship.idreqtag = R.idreqtag
                            ''')
        row_headers=[x[0] for x in cursor.description]
        rv = cursor.fetchall()
        json_data=[]

        for result in rv:
            json_data.append(dict(zip(row_headers, result)))

        return json.dumps(json_data, default=json_converter)

    def post(self):
        """Post to scholarships.

        Arguments:
            keywords: Keywords separated by commas.
            major (required): academic major as listed in database (example: actuarial-science)

        Returns:
            json: Data for filtered scholarships

        """
        # Parse request parameters
        parser = reqparse.RequestParser()
        parser.add_argument('keywords', help="Keywords separated by commas.")
        parser.add_argument('major', required=True, help="Academic major. Must be direct match to the data in the database.")
        parser.add_argument('min_amount', help="Minimum limit on scholarship amount.")
        parser.add_argument('max_amount', help="Maximum limit on scholarship amount.")
        parser.add_argument('sex', help="Male or Female. Other will just return all.")
        parser.add_argument('citizenship', help="True - citizenship required. False - citizenship not required or unknown")
        args = parser.parse_args()

        # Build query parts
        query = '''SELECT * FROM Scholarship INNER JOIN Reqtag R ON Scholarship.idreqtag = R.idreqtag'''
        filters = []
        parameters = []

        if args['major']:
            filters.append(''' WHERE major = %s ''')
            parameters.append(args['major'])

        # Add keyword search to query
        if args['keywords']:
            for i, word in enumerate(args['keywords'].split(',')):
                filters.append(''' AND (CONCAT(description, name)) LIKE CONCAT("%%", %s, "%%") ''')
                parameters.append(word)

        # Add min amount to query
        if args['min_amount']:
            filters.append(''' AND amount >= %s  ''')
            parameters.append(args['min_amount'])

        # Add max amount to query
        if args['max_amount']:
            filters.append(''' AND amount <= %s ''')
            parameters.append(args['max_amount'])

        # Add sex to query
        if args['sex']:
            if args['sex'] == "Female":
                param = 1
            elif args['sex'] == "Male":
                param = 2

            if param:
                parameters.append(param)
                filters.append(''' AND sex = %s ''')

        # Add citizenship to query
        if args['citizenship']:
            if args['citizenship'] == 'True':
                filters.append(''' AND citizenship =  1''')
            elif args['citizenship'] == 'False':
                filters.append(''' AND (citizenship IS NULL OR citizenship != 1)''')

        # Only get data where the due date has not passed
        date_today = date_today_s()
        filters.append('AND (deadline >= %s)')
        parameters.append(date_today)


        # Combine query
        for filt in filters:
            query += filt

        parameters = tuple(i for i in parameters)

        # Run query
        db, cursor = db_connect()
        print(query % parameters, flush=True)
        cursor.execute(query, parameters)
        row_headers = [x[0] for x in cursor.description]
        rv = cursor.fetchall()
        json_data = []

        for result in rv:
            json_data.append(dict(zip(row_headers,result)))

        return json.dumps(json_data, default=json_converter)


api.add_resource(Scholarships, '/scholarships')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
