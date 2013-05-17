import datetime
import re
from docutils.core import publish_parts
from pyramid.response import Response
from pyramid.renderers import get_renderer
from .security import USERS

from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    )

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Page,
    User,
    Patient,
    Medic,
    Director,
    Allergy,
    MedicalHistory,
    Views
    )


@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='Home').first()

    return dict(title='Home', main=main , page = page,
                user=request.user)
    
@view_config(route_name='about_us', renderer='templates/home.pt')
def about_us(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='User').first()

    return dict(title='About Us', 
                main=main,
                page = page,
                user=request.user)
    
@view_config(route_name='contact_us', renderer='templates/home.pt')
def contact_us(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='Contact').first()

    return dict(title='Contact Us', 
                main=main,
                page = page,
                user=request.user)
    

@view_config(route_name='why_create_user', renderer='templates/home.pt')
def why_create_user(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='User').first()

    return dict(title='Why Create a User Account',
                main=main ,
                page = page,
                user=request.user)
    
@view_config(route_name='new_user', renderer='templates/register_user.pt')
def create_user(request):
    main = get_renderer('templates/template.pt').implementation()
    message = ''
    if 'form.submitted' in request.params:
        username_entered = request.params['username']
        exists = DBSession.query(User).filter(User.login == username_entered).count()
        if username_entered and not exists:
            new_user = User(login = username_entered,
                            password = request.params['password'],
                            first_name = request.params['firstname'],
                            middle_name = request.params['middlename'],
                            last_name = request.params['lastname'],
                            gender = request.params['gender'],
                            birthday = datetime.date(int(request.params['year']),int(request.params['month']),int(request.params['day'])),
                            primary_language = request.params['primary_langauge'],
                            secondary_language = request.params['secondary_langauge'],
                            social_security = request.params['social_security'],
                            street = request.params['street'],
                            city = request.params['city'],
                            state = request.params['state'],
                            zipcode = request.params['zipcode'],
                            phone = request.params['phonenumber'],
                            email = request.params['email'],
                            )
            DBSession.add(new_user)
        elif not username_entered:
            message = 'Please enter a Login'
        elif exists:
            message = 'Login exists, please enter a different Login: {}'.format(exists)

    
    return dict(title='Create a User Account',
                main=main,
                message=message,
                user=request.user)
    
@view_config(route_name='edit_user', renderer='templates/edit_user.pt')
def edit_user(request):
    main = get_renderer('templates/template.pt').implementation()
    message =''
    edit_user = DBSession.query(User).filter(User.login == request.user['user_account'].login).first()

    if 'form.submitted' in request.params:
        edit_user.password = request.params['password']
        edit_user.first_name = request.params['firstname']
        edit_user.middle_name = request.params['middlename']
        edit_user.last_name = request.params['lastname']
        edit_user.gender = request.params['gender']
        edit_user.birthday = datetime.date( int(request.params['year']), int(request.params['month']), int(request.params['day']) )
        edit_user.primary_language = request.params['primary_langauge']
        edit_user. secondary_language = request.params['secondary_langauge']
        edit_user. social_security = request.params['social_security']
        edit_user. street = request.params['street']
        edit_user.city = request.params['city']
        edit_user.state = request.params['state']
        edit_user.zipcode = request.params['zipcode']
        edit_user.phone = request.params['phonenumber']
        edit_user.email = request.params['email']
        DBSession.add(edit_user)
        message = 'Account edited'

    
    
    return dict(title = 'Edit User Account',
                main = main,
                message=message,
                edit_user = edit_user,
                user=request.user)

@view_config(route_name='view_user', renderer='templates/view_user.pt')
def view_user(request):
    main = get_renderer('templates/template.pt').implementation()
    message =''
    
    return dict(title = 'View User Account',
                main = main,
                message=message,
                user=request.user)

    
@view_config(route_name='why_register_patient', renderer='templates/home.pt')
def why_register_patient(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='Patient').first()

    return dict(title='Why Register A Patient Account',
                main=main ,
                page = page,
                user=request.user)

@view_config(route_name='register_patient', renderer='templates/register_patient.pt')
def register_patient(request):
    main = get_renderer('templates/template.pt').implementation()
    
    message = ''
    if 'form.submitted' in request.params:
        username_entered = request.params['username']
        exists = DBSession.query(Patient).filter(Patient.user == username_entered).count()
        if username_entered and not exists:
            new_user = Patient(user = username_entered,
                               rfidtag = request.params['rfid'],
                               primary_physician = request.params['doctor'],
                               )
            DBSession.add(new_user)
            message = 'Thank you for registering'
        elif not username_entered:
            message = 'Please enter a Login'
        elif exists:
            message = 'Patient Record exists for this user account, please sign into different account and contact an admin with any questions: {}'.format(exists)

    return dict(title='Create a Patient Account',
                main=main,
                message=message,
                user=request.user)
    
@view_config(route_name='edit_patient', renderer='templates/edit_patient.pt')
def edit_patient(request):
    main = get_renderer('templates/template.pt').implementation()
    message =''
    edit_patient = DBSession.query(Patient).filter(Patient.user == request.user['user_account'].login).first()

    if 'form.submitted' in request.params:
        rfidused = DBSession.query(Patient).filter(Patient.rfidtag==request.params['rfid'] and not Patient.user == request.user['user_account'].login).count()
        if not rfidused:
            edit_patient.rfidtag = request.params['rfid']
            edit_patient.primary_physician = request.params['doctor']
            DBSession.add(edit_patient)
            message = 'Account edited'
        if rfidused:
            message = "RFID is used by different Patient"
        
        
    return dict(title = 'Edit Patient Information',
                main = main,
                message=message,
                edit_patient = edit_patient,
                user=request.user)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
@view_config(route_name='edit_allergies', renderer='templates/edit_allergies.pt')
def edit_allergies(request):
    main = get_renderer('templates/template.pt').implementation()
    message =''
    form = ''
    username = request.user['user_account'].login
        
    if 'form.new' in request.params:
        form = "new"

    if 'form.delete' in request.params:
        list = eval(request.params['edit_allergen'])
        exist = DBSession.query(Allergy).filter_by(user = list[0]).filter_by(allergy = list[1]).first()
        if exist:
            DBSession.delete(exist)
        if not exist:
            message = "Sorry, but there seems to be a problem with the database, please contact your system administrator"


    if 'form.submit' in request.params:
        form = ''
        list = [username,request.params['new_allergen']]
        exist = DBSession.query(Allergy).filter_by(user = list[0]).filter_by(allergy = list[1]).first()
        if not exist:
            print("exist")
            DBSession.add(
                          Allergy(
                                  user=list[0],
                                  allergy=list[1]
                                  )
                          )
        if exist:
            print("exist")
            message = "Allergen already exists for that user"
        
    allergies_query = DBSession.query(Allergy).filter(Allergy.user == username).all()
    if allergies_query:
        allergies_list = [[allergy.user, allergy.allergy] for allergy in allergies_query]
    else:
        allergies_list = [username,'Nothing']
        
        
    return dict(title = 'Edit Allergies',
                main = main,
                message=message,
                form=form,
                allergies=allergies_list,
                edit_patient = edit_patient,
                user=request.user)    
    
@view_config(route_name='edit_history', renderer='templates/edit_history.pt')
def edit_history(request):
    main = get_renderer('templates/template.pt').implementation()
    message =''
    form = ''
    username = request.user['user_account'].login
        
    if 'form.new' in request.params:
        form = "new"

    if 'form.delete' in request.params:
        list = eval(request.params['edit_allergen'])
        exist = DBSession.query(MedicalHistory).filter_by(user = list[0]).filter_by(event = list[1]).first()
        if exist:
            DBSession.delete(exist)
        if not exist:
            message = "Sorry, but there seems to be a problem with the database, please contact your system administrator"
    if 'form.submit' in request.params:
        list = [username,request.params['new_history']]
        exist = DBSession.query(MedicalHistory).filter_by(user = list[0]).filter_by(event = list[1]).first()
        if not exist:
            print("exist")
            DBSession.add(
                          MedicalHistory(
                                  user=list[0],
                                  event=list[1]
                                  )
                          )
        if exist:
            message = "Event already exists for that user"
            print("exist")
    
    
    history_query = DBSession.query(MedicalHistory).filter(MedicalHistory.user == username).all()
    if history_query:
        i = 1
        history_list = []
        for history in history_query:
            history_list.append([i,history.user, history.event])
    else:
        history_list = [0,username,'Nothing']

        
        
    return dict(title = 'Edit Past Medical History',
                main = main,
                message=message,
                form=form,
                history=history_list,
                user=request.user)    

    

    
@view_config(route_name='view_patient', renderer='templates/view_patient.pt')
def view_patient(request):
    main = get_renderer('templates/template.pt').implementation()
    message =''
    patient = DBSession.query(Patient.user,
                              Patient.rfidtag,
                              Patient.primary_physician,
                              User.first_name).\
                              join(User).\
                              filter(Patient.user == request.user['user_account'].login).one()
    patient_data = [patient.user,patient.rfidtag,patient.primary_physician,patient.first_name]
    
    return dict(title = 'View Patient Account',
                main = main,
                message=message,
                patient=patient,
                user=request.user)
    
    
    
@view_config(route_name='patient_history', renderer='templates/patient_history.pt')
def patient_history(request):
    main = get_renderer('templates/template.pt').implementation()
    message =''
    view_list = DBSession.query(Views).\
                              filter_by(patient = request.user['user_account'].login).all()
    view_data = [[patient.patient,patient.medic,patient.time]for patient in view_list]
    
    return dict(title = 'Patient Viewed History',
                main = main,
                message=message,
                view_data=view_data,
                user=request.user)
    
@view_config(route_name='why_register_medic', renderer='templates/home.pt')
def why_register_medic(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='Medic').first()

    return dict(title='Why Register A Medic Account',
                main=main ,
                page = page,
                user=request.user)
    
@view_config(route_name='register_medic', renderer='templates/register_medic.pt')
def register_medic(request):
    main = get_renderer('templates/template.pt').implementation()
    
    message = ''
    if 'form.submitted' in request.params:
        username_entered = request.params['user']
        exists = DBSession.query(Medic).filter(Medic.user == username_entered).count()
        if username_entered and not exists:
            new_user = Medic(user = username_entered,
                               training_level = request.params['training_level'],
                               cert_number = request.params['cert_number'],
                               )
            DBSession.add(new_user)
            message = 'Thank you for registering'
        elif not username_entered:
            message = 'Please enter a Login'
        elif exists:
            message = 'Medic Record exists for this user account, please sign into different account and contact an admin with any questions: {}'.format(exists)

    return dict(title='Create a Medic Account',
                main=main,
                message=message,
                user=request.user)
    
    
@view_config(route_name='edit_medic', renderer='templates/edit_medic.pt')
def edit_medic(request):
    main = get_renderer('templates/template.pt').implementation()
    edit_user = DBSession.query(Medic).filter(Medic.user == request.user['user_account'].login).one()

    message = ''
    if 'form.submitted' in request.params:
        username_entered = request.params['user']
        edit_user.training_level = request.params['training_level'],
        edit_user.cert_number = request.params['cert_number'],
        DBSession.add(edit_user)
        message = 'Medic Edited'
        
    return dict(title='Edit a Medic Account',
                main=main,
                message=message,
                edit_user=edit_user,
                user=request.user)
    
    
@view_config(route_name='view_medic', renderer='templates/view_medic.pt')
def view_medic(request):
    main = get_renderer('templates/template.pt').implementation()
    message =''
    medic = DBSession.query(Medic.user,
                              Medic.training_level,
                              Medic.cert_number,
                              User.first_name).\
                              join(User).\
                              filter(Medic.user == request.user['user_account'].login).one()
    medic_data = [medic.user,medic.training_level,medic.cert_number,medic.first_name]
    
    return dict(title = 'View Medic Account',
                main = main,
                message=message,
                medic_data=medic_data,
                user=request.user)
    
@view_config(route_name='view_patient_as_medic', renderer='templates/view_patient_as_medic.pt')
def view_patient_as_medic(request):
    main = get_renderer('templates/template.pt').implementation()
    message =''
    patient = ['','']
    form =''
    users = DBSession.query(Patient.user).all()
    users_list = [us.user for us in users]
    
    if 'selected_user' in request.params:
        form = request.params['selected_user']
        patient = DBSession.query(Patient,User).\
                                  join(User).\
                                  filter(Patient.user == form).first()
        if patient:
            form = 'select'
            DBSession.add(
                          Views(
                                patient = patient[0].user,
                                medic = request.user['user_account'].login,
                                time = datetime.datetime.now()
                                ))

    
    return dict(title = 'View Patient Account',
                main = main,
                message=message,
                form=form,
                patient_data=patient[0],
                users_list=users_list,
                user_data=patient[1],
                user=request.user)
    
@view_config(route_name='medic_history', renderer='templates/medic_history.pt')
def medic_history(request):
    main = get_renderer('templates/template.pt').implementation()
    message =''
    view_list = DBSession.query(Views).\
                              filter_by(medic = request.user['user_account'].login).all()
    view_data = [[medic.patient,medic.medic,medic.time]for medic in view_list]
    
    return dict(title = 'Medic Viewing History',
                main = main,
                message=message,
                view_data=view_data,
                user=request.user)
    
@view_config(route_name='why_register_director', renderer='templates/home.pt')
def why_register_director(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='Director').first()

    return dict(title='Why Register A Medical Director Account',
                main=main ,
                page = page,
                user=request.user)

@view_config(route_name='register_director', renderer='templates/register_director.pt')
def register_director(request):
    main = get_renderer('templates/template.pt').implementation()
    
    message = ''
    if 'form.submitted' in request.params:
        username_entered = request.params['user']
        exists = DBSession.query(Director).filter(Director.user == username_entered).count()
        if username_entered and not exists:
            new_user = Director(user = username_entered,
                               
                               )
            DBSession.add(new_user)
            message = 'Thank you for registering'
        elif not username_entered:
            message = 'Please enter a Login'
        elif exists:
            message = 'Medical Director Record exists for this user account, please sign into different account and contact an admin with any questions: {}'.format(exists)

    return dict(title='Create a Medical Director Account',
                main=main,
                message=message,
                user=request.user)



@view_config(route_name='edit_director', renderer='templates/edit_director.pt')
def edit_director(request):
    main = get_renderer('templates/template.pt').implementation()
    edit_user = DBSession.query(Director).filter(Director.user == request.user['user_account'].login).one()

    message = ''
    if 'form.submitted' in request.params:
        username_entered = request.params['user']
        DBSession.add(edit_user)
        message = 'Medic Edited'
        
    return dict(title='Edit a Medical Director Account',
                main=main,
                message=message,
                edit_user=edit_user,
                user=request.user)

@view_config(route_name='view_director', renderer='templates/view_director.pt')
def view_director(request):
    main = get_renderer('templates/template.pt').implementation()
    message =''
    medic = DBSession.query(Director.user,
                              User.first_name).\
                              join(User).\
                              filter(Director.user == request.user['user_account'].login).one()
    director_data = [medic.user,medic.first_name]
    
    return dict(title = 'View Medical Director Account',
                main = main,
                message=message,
                director_data=director_data,
                user=request.user)



@view_config(route_name='view_patient_as_director', renderer='templates/view_patient_as_director.pt')
def view_patient_as_director(request):
    main = get_renderer('templates/template.pt').implementation()
    message =''
    patient = ['','']
    form =''
    users = DBSession.query(Patient.user).all()
    users_list = [us.user for us in users]
    
    if 'selected_user' in request.params:
        form = request.params['selected_user']
        patient = DBSession.query(Patient,User).\
                                  join(User).\
                                  filter(Patient.user == form).first()
        if patient:
            form = 'select'
            DBSession.add(
                          Views(
                                patient = patient[0].user,
                                medic = request.user['user_account'].login,
                                time = datetime.datetime.now()
                                ))

    
    return dict(title = 'View Patient Account',
                main = main,
                message=message,
                form=form,
                patient_data=patient[0],
                users_list=users_list,
                user_data=patient[1],
                user=request.user)
    

@view_config(route_name='view_patient_history', renderer='templates/view_patient_history.pt')
def view_patient_history(request):
    main = get_renderer('templates/template.pt').implementation()
    message =''
    view_data = []
    users = DBSession.query(Patient.user).all()
    users_list = [us.user for us in users]
    
    if 'select' in request.params:
        name = request.params['selected_user']
        view_list = DBSession.query(Views).\
                                  filter_by(patient = name).all()
        view_data = [[patient.patient,patient.medic,patient.time]for patient in view_list]
    
    return dict(title = 'Patient Viewed History',
                main = main,
                message=message,
                users=users_list,
                view_data=view_data,
                user=request.user)



@view_config(route_name='view_medic_as_director', renderer='templates/view_medic_as_director.pt')
def view_medic_as_director(request):
    main = get_renderer('templates/template.pt').implementation()
    message =''
    form = ''
    medic = ['','']
    users = DBSession.query(Medic.user).all()
    users_list = [us.user for us in users]
    
    if 'select' in request.params:
        form = request.params['selected_user']
        medic = DBSession.query(Medic,User).\
                                  join(User).\
                                  filter(Medic.user == form).one()
    
    return dict(title = 'View Medic Account',
                main = main,
                message=message,
                users=users_list,
                form=form,
                medic_data=medic[0],
                user_data=medic[1],
                user=request.user)


@view_config(route_name='view_medic_history', renderer='templates/view_medic_history.pt')
def view_medic_history(request):
    main = get_renderer('templates/template.pt').implementation()
    message =''
    view_data = []
    users = DBSession.query(Medic.user).all()
    users_list = [us.user for us in users]
    
    if 'select' in request.params:
        name = request.params['selected_user']
        view_list = DBSession.query(Views).\
                                  filter_by(medic = name).all()
        view_data = [[medic.patient,medic.medic,medic.time]for medic in view_list]
    
    return dict(title = 'Medic Viewing History',
                main = main,
                message=message,
                users=users_list,
                view_data=view_data,
                user=request.user)

@view_config(route_name='view_all_users', renderer='templates/view_all_accounts.pt')
def view_all_users(request):
    main = get_renderer('templates/template.pt').implementation()
    all_users = DBSession.query(User).all()
    headers = [column.name for column in User.__table__.columns]
    
    return dict(title='View All Users',
                main=main ,
                all_users = all_users,
                headers = headers,
                user=request.user)
    
@view_config(route_name='view_all_patients', renderer='templates/view_all_accounts.pt')
def view_all_patients(request):
    main = get_renderer('templates/template.pt').implementation()
    all_users = DBSession.query(Patient).all()
    headers = [column.name for column in Patient.__table__.columns]
    
    return dict(title='View All Patients',
                main=main ,
                all_users = all_users,
                headers = headers,
                user=request.user)
    
@view_config(route_name='view_all_medics', renderer='templates/view_all_accounts.pt')
def view_all_medics(request):
    main = get_renderer('templates/template.pt').implementation()
    all_users = DBSession.query(Medic).all()
    headers = [column.name for column in Medic.__table__.columns]

    
    return dict(title='View All Medics',
                main=main ,
                all_users = all_users,
                headers = headers,
                user=request.user)
    
@view_config(route_name='view_all_directors', renderer='templates/view_all_accounts.pt')
def view_all_directors(request):
    main = get_renderer('templates/template.pt').implementation()
    all_users = DBSession.query(Director).all()
    headers = [column.name for column in Director.__table__.columns]

    
    return dict(title='View All Directors',
                main=main ,
                all_users = all_users,
                headers = headers,
                user=request.user)
    
@view_config(route_name='login', renderer='templates/login.pt')
@forbidden_view_config(renderer='templates/login.pt')
def login(request):
    main = get_renderer('templates/template.pt').implementation()
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        login_tried = DBSession.query(User.login, User.password).filter(User.login == login).first()
        if login_tried:
            if login_tried[1] == password:
                headers = remember(request, login)
                return HTTPFound(location = came_from,
                             headers = headers)
        message = 'Failed login'

    return dict(
        main = main,
        title = 'Login',
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        user=request.user)

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('home'),
                     headers = headers,
                     )

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_senior_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

