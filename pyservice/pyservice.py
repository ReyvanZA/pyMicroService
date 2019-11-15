try:
    from cheroot.wsgi import Server as WSGIServer, PathInfoDispatcher
except ImportError:
    from cherrypy.wsgiserver import CherryPyWSGIServer as WSGIServer, WSGIPathInfoDispatcher as PathInfoDispatcher


from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

import random
import json
import db as model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.sqlite'
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

#db.session.add(model.Customer(f'Test{random.randrange(100,999)}','Test',f'er{random.randrange(100,999)}'))

#db.session.add(model.Customer(f'Test{random.randrange(100,999)}','Test',f'er{random.randrange(100,999)}'))

#db.session.commit()

@auth.get_password
def get_password(username):
    if username == 'user':
        return 'password'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.route('/')
def index():
    return ""

@app.route('/api/customer',methods=['GET'])
@auth.login_required
def customer():
    customers = db.session.query(model.Customer).all()
    result = '['
    for customer in customers:
        result += json.dumps(customer.to_dict()) + ','

    result = result[:-1]    

    return  result + ']'

if __name__ == '__main__':
    d = PathInfoDispatcher({'/': app})
    server = WSGIServer(('0.0.0.0', 80), d)

    try:
      server.start()
    except KeyboardInterrupt:
      server.stop()





        