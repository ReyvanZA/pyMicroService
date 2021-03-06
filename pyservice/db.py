from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, DateTime
from sqlalchemy import MetaData
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm.attributes import QueryableAttribute

import datetime
import random

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.sqlite'
db = SQLAlchemy(app)

# JSON base model
class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self, show=None, _hide=[], _path=None):
        """Return a dictionary representation of this model."""

        show = show or []

        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
        default = self._default_fields if hasattr(self, "_default_fields") else []
        default.extend(['id', 'modified_at', 'created_at'])

        if not _path:
            _path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split(".", 1)[0] == _path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != ".":
                    item = ".%s" % item
                item = "%s%s" % (_path, item)
                return item

            _hide[:] = [prepend_path(x) for x in _hide]
            show[:] = [prepend_path(x) for x in show]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        ret_data = {}

        for key in columns:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                ret_data[key] = getattr(self, key)

        for key in relationships:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                _hide.append(check)
                is_list = self.__mapper__.relationships[key].uselist
                if is_list:
                    items = getattr(self, key)
                    if self.__mapper__.relationships[key].query_class is not None:
                        if hasattr(items, "all"):
                            items = items.all()
                    ret_data[key] = []
                    for item in items:
                        ret_data[key].append(
                            item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        )
                else:
                    if (
                        self.__mapper__.relationships[key].query_class is not None
                        or self.__mapper__.relationships[key].instrument_class
                        is not None
                    ):
                        item = getattr(self, key)
                        if item is not None:
                            ret_data[key] = item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        else:
                            ret_data[key] = None
                    else:
                        ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            if not hasattr(self.__class__, key):
                continue
            attr = getattr(self.__class__, key)
            if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    ret_data[key] = val.to_dict( show=list(show)
                    , _hide=list(_hide)
                    , _path=("%s.%s" % (_path, key.lower())))
                else:
                    try:
                        ret_data[key] = json.loads(json.dumps(val))
                    except:
                        pass

        return ret_data


#Data ORM tables
#Take a look
#   https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/
class Customer(BaseModel):
    __tablename__ = 'Customer'

    cst_id = Column(Integer, primary_key=True)
    cst_abbreviation = Column(String)
    cst_firstName = Column(String)
    cst_lastName = Column(String)

    def __init__(self, Abbr, First, Last):
        self.cst_abbreviation = Abbr
        self.cst_firstName = First
        self.cst_lastName = Last

    _default_fields = [
        'cst_id',
        'cst_abbreviation'
    ]

class Address(BaseModel):
    __tablename__ = 'Address'

    add_id = Column(Integer, primary_key=True)
    add_abbreviation = Column(String)
    add_name = Column(String)
    add_street = Column(String)
    add_area = Column(String)
    add_town = Column(String)
    add_province = Column(String)
    add_postalcode = Column(Integer)
    add_Telephone1 = Column(String)
    add_cstid = Column(Integer, ForeignKey('Customer.cst_id'))

    
#Service Tables

class User(db.Model):
    __tablename__ = 'User'

    usr_id = Column(Integer, primary_key=True)
    usr_login = Column(String(50))
    usr_name = Column(String(50))
    usr_email = Column(String(100))
    usr_password = Column(String(200))
    usr_status = Column(Integer)
    usr_created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

class Group(db.Model):
    __tablename__ = 'Group'

    grp_id = Column(Integer, primary_key=True)
    grp_name = Column(String(20))
    grp_description = Column(String)
    grp_status = Column(Integer)


class UserGroup(db.Model):
    __tablename__ = 'UserGroup'

    ugr_id = Column(Integer, primary_key=True)
    ugr_usrid = Column(Integer, ForeignKey('User.usr_id'))
    ugr_grpid = Column(Integer, ForeignKey('Group.grp_id'))


def createdb():
    """Create some random data for testing"""
    db.session.add(Customer(f'Test{random.randrange(100,999)}','Test',f'er{random.randrange(100,999)}'))
    db.session.add(Customer(f'Test{random.randrange(100,999)}','Test',f'er{random.randrange(100,999)}'))
    
    db.session.commit()


if __name__ == "__main__":
    engine = create_engine('sqlite:///example.sqlite', echo=True)
    
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f'Datebase Created: {database_exists(engine.url)}')    
    else:
        print(f'Database Already exists.')

    db.metadata.create_all(engine)

    createdb()
    
    





