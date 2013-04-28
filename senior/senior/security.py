from pyramid.security import (
    unauthenticated_userid,
    )

from .models import (
    DBSession,
    User,
    Medic,
    Patient,
    Director,
    )


USERS = {'admin'   :'admin',
         'director':'director',
         'medic'   :'medic',
         'patient' :'patient',
         'user'    :'user',
          }
GROUPS = {'admin'  :['admins'],
         'director':['directors'],
         'medic'   :['medics'],
         'patient' :['patients'],
         'user'    :['users'],
          }

def get_user(request):
    """Gets the username and the groups the user is associated with"""
    userid = unauthenticated_userid(request),
    print(userid)
    if userid:
        user_account = DBSession.query(User).filter(User.login == userid[0]).first()
        if user_account:
            medic    =  DBSession.query(Medic).filter(Medic.user == user_account.login).first()
            if not medic:
                medic = False
            patient  =  DBSession.query(Patient).filter(Patient.user == user_account.login).first()
            if not patient:
                patient = False
            director =  DBSession.query(Director).filter(Director.user == user_account.login).first()
            if not director:
                director = False
                
            return dict(
                        user_account=user_account, 
                        is_medic   =medic,
                        is_patient =patient,
                        is_director=director,
                        )
    return None

def groupfinder(userid, request):
    user_account = request.user
    group = ['Guest']
    if user_account:
        groups = ['User']
        if user_account['is_medic']:
            groups = groups[:] + ['Medic']
        if user_account['is_patient']:
            groups = groups[:] + ['Patient']
        if user_account['is_director']:
            groups = groups[:] + ['Director']
    return groups