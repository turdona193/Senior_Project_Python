from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    Date,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

from pyramid.security import (
    Allow,
    Everyone,
    ALL_PERMISSIONS,

    )
class RootFactory(object):
    __acl__ = [ (Allow, Everyone   , 'Guest'),
                (Allow, 'users'    , 'user') ,
                (Allow, 'patients' , 'patient') ,
                (Allow, 'medics'   , 'medic') ,
                (Allow, 'directors', 'user') ,
                (Allow, 'admins'   ,ALL_PERMISSIONS ) ,
                ]
    def __init__(self, request):
        pass

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Allergy(Base):
    __tablename__ = 'allergy'
    user = Column(Text, ForeignKey('patient.user'), primary_key=True)
    allergy = Column(Text, primary_key=True)
    def __init__(self,user,allergy):
        self.user = user
        self.allergy = allergy

class Director(Base):
    __tablename__ = 'medical_director'
    user = Column(Text, ForeignKey('patient.user'), primary_key=True)
    def __init__(self,user,):
        self.user = user
        
class Medic(Base):
    __tablename__ = 'medic'
    user = Column(Text, ForeignKey('user.login'), primary_key=True)
    training_level = Column(Text)
    cert_number = Column(Text)
    def __init__(self,user,training_level,cert_number):
        self.user = user
        self.training_level = training_level
        self.cert_number = cert_number
        
class MedicalHistory(Base):
    __tablename__ = 'medicalhistory'
    user = Column(Text, ForeignKey('patient.user'), primary_key=True)
    event = Column(Text, primary_key=True)
    def __init__(self,user,event):
        self.user = user
        self.event = event
        
class Page(Base):
    """ The SQLAlchemy declarative model class for a Page object. """
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    data = Column(Text)

    def __init__(self, name, data):
        self.name = name
        self.data = data        

class Patient(Base):
    __tablename__ = 'patient'
    user = Column(Text, ForeignKey('user.login'), primary_key=True)
    rfidtag  = Column(Text, unique=True)

    #pastmedicalhistory 
    #allergies
    primary_physician = Column(Text)
    def __init__(self, user,rfidtag, primary_physician):
        self.user = user
        self.rfidtag = rfidtag
        self.primary_physician = primary_physician

class User(Base):
    __tablename__ = 'user'
    login     = Column(Text, primary_key=True)
    password  = Column(Text)
    first_name = Column(Text)
    middle_name = Column(Text)
    last_name  = Column(Text)
    gender    = Column(Text)
    birthday  = Column(Date)
    primary_language   = Column(Text)
    secondary_language = Column(Text)
    social_security = Column(Integer)
    phone = Column(Text)
    street = Column(Text)
    city =Column(Text)
    state = Column(Text)
    zipcode = Column(Integer) 
    email = Column(Text)
       
    def __init__(self, login, password, first_name, middle_name, last_name, gender, birthday, primary_language, secondary_language, social_security, phone,street,city,state,zipcode,email):
        self.login = login
        self.password = password
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.gender = gender
        self.birthday = birthday
        self.primary_language = primary_language
        self.secondary_language = secondary_language
        self.social_security = social_security
        self.phone = phone
        self.street = street
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.email = email
