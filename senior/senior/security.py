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
def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])