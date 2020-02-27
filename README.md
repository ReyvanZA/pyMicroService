## pyMicroService
A simple micro service for exposing data via a secure restful interface

This is a learning project for me, and I have no idea what direction it is going to take. All I want to do for now is to create a secure way of retrieving data from a data source, and expose it via a RESTful service to the world. 

It is dirty!

I'm not that PEPpy (https://www.python.org/dev/peps), but I'm enthusiastic 

# Code example

    @app.route('/api/customer',methods=['GET'])
    @auth.login_required
    def customer():
        """Returns a json list of all customers"""
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

# Features
* JSON output of sqlalchemy results
* Basic Authentication
* SSL (Self signed)  
  --https://docs.cherrypy.org/en/latest/deploy.html 
* Dev (local.py) and Production (config.py) settings


# Todo
* Dynamic Users/groups stored in the database

# Kudo's
Base on the blog post by Miguel Grinberg (among others).
https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask 


Thanks to Alan Hamlett for the JSONinification of the sqlalchemy results
https://wakatime.com/blog/32-flask-part-1-sqlalchemy-models-to-json 

Then going advanced deployement (Structuring a Flak-RESTPlus web service for production) by Greg Obinna
https://www.freecodecamp.org/news/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563/ 

# Requires (+)
* FLask as the micro web framewrok https://www.palletsprojects.com/p/flask/ 
* SQLAlchemy ORM to expose the database https://www.sqlalchemy.org/ 
* CherryPy WSGI server to server the service :) https://cherrypy.org/ 


+ Not an extensive list. Keep an eye on the requirements file



