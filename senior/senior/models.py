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



class Page(Base):
    """ The SQLAlchemy declarative model class for a Page object. """
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    data = Column(Text)

    def __init__(self, name, data):
        self.name = name
        self.data = data

class Users(Base):
    __tablename__ = 'user'
    login     = Column(Text, primary_key=True)
    password  = Column(Text)
    firstname = Column(Text)
    middlename = Column(Text)
    lastname  = Column(Text)
    gender    = Column(Text)
    birthday  = Column(Date)
    primarylanguage   = Column(Text)
    secondarylanguage = Column(Text)
    socialsecurity = Column(Text)
    phone = Column(Text)
    street = Column(Text)
    city =Column(Text)
    state = Column(Text)
    zipcode = Column(Integer) 
       
    def __init__(self, login, password, lastname, firstname, gender, birthday, primarylanguage, secondarylanguage, socialsecurity, phone,street,city,state,zipcode):
        self.login = login
        self.password = password
        self.lastname = lastname
        self.firstname = firstname
        self.gender = gender
        self.birthday = birthday
        self.primarylanguage = primarylanguage
        self.secondarylanguage = secondarylanguage
        self.socialsecurity = socialsecurity
        self.phone = phone
        self.street = street
        self.city = city
        self.state = state
        self.zipcode = zipcode

class Medic(Base):
    __tablename__ = 'medic'
    user = Column(Text, ForeignKey('user.login'), primary_key=True)
    traininglevel = Column(Text)
    certnumber = Column(Text)
    def __init__(self,user,traininglevel,certnumber):
        self.user = user
        self.traininglevel = traininglevel
        self.certnumber = certnumber
        
class Patient(Base):
    __tablename__ = 'patient'
    user = Column(Text, ForeignKey('user.login'), primary_key=True)
    #pastmedicalhistory 
    #allergies
    physician = Column(Text)
    def __init__(self, user, physician):
        self.user = user
        self.physician = physician
    
class Allergy(Base):
    __tablename__ = 'allergy'
    user = Column(Text, ForeignKey('patient.user'), primary_key=True)
    allergy = Column(Text, primary_key=True)
    def __init__(self,user,allergy):
        self.user = user
        self.allergy = allergy
        
class MedicalHistory(Base):
    __tablename__ = 'medicalhistory'
    user = Column(Text, ForeignKey('patient.user'), primary_key=True)
    event = Column(Text, primary_key=True)
    def __init__(self,user,event):
        self.user = user
        self.event = event
