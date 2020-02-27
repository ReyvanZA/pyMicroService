import config
try:
    from cheroot.wsgi import Server as WSGIServer, PathInfoDispatcher
    from cheroot.ssl.builtin import BuiltinSSLAdapter
except ImportError:
    from cherrypy.wsgiserver import CherryPyWSGIServer as WSGIServer, WSGIPathInfoDispatcher as PathInfoDispatcher

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

import json
import db as model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.sqlite'
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

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

#Take a look at https://stackoverflow.com/questions/48073635/flask-httpauth-user-access-levels 

@app.route('/api/customer',methods=['GET'])
@auth.login_required
def customer():
    """Returns a json list of all customers"""
    customers = model.Customer.query.all()
    result = '['

    if len(customers) == 0 :
        return '[]'

    for customer in customers:
        result += json.dumps(customer.to_dict()) + ','

    result = result[:-1]    

    return  result + ']'


#Take a look on running the cherry server:
#   https://stackoverflow.com/questions/55366395/how-to-run-a-flask-app-on-cherrypy-wsgi-server-cheroot-using-https 
#   https://www.digitalocean.com/community/tutorials/how-to-deploy-python-wsgi-applications-using-a-cherrypy-web-server-behind-nginx 
#         

if __name__ == '__main__':
    """Run the cherry server"""
    d = PathInfoDispatcher({'/': app})
    server = WSGIServer(('0.0.0.0', 8000), d)

    path = config.settings['sslPath']

    server.ssl_adapter = BuiltinSSLAdapter(certificate=f'{path}cert.pem', private_key=f'{path}privkey.pem')
    
    try:
      server.start()
    except KeyboardInterrupt:
      server.stop()





        