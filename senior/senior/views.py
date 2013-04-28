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
    
@view_config(route_name='new_user', renderer='templates/newuser.pt')
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
    
@view_config(route_name='edit_user', renderer='templates/edituser.pt')
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

@view_config(route_name='view_user', renderer='templates/viewuser.pt')
def view_user(request):
    main = get_renderer('templates/template.pt').implementation()
    message =''
    
    return dict(title = 'Edit User Account',
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
    
@view_config(route_name='why_register_medic', renderer='templates/home.pt')
def why_register_medic(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='Medic').first()

    return dict(title='Why Register A Medic Account',
                main=main ,
                page = page,
                user=request.user)
    
@view_config(route_name='why_register_director', renderer='templates/home.pt')
def why_register_director(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='Director').first()

    return dict(title='Why Register A Medical Director Account',
                main=main ,
                page = page,
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

