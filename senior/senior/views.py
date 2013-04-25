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
    
    Users,
    )


@view_config(route_name='home', renderer='templates/home.pt')
def Home(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='Home').first()

    return dict(title='Home', main=main , page = page,
                logged_in=authenticated_userid(request))
    
@view_config(route_name='about_us', renderer='templates/home.pt')
def AboutUs(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='User').first()

    return dict(title='About Us', 
                main=main,
                page = page,
                logged_in=authenticated_userid(request))
    
@view_config(route_name='contact_us', renderer='templates/home.pt')
def ContactUs(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='Contact').first()

    return dict(title='Contact Us', 
                main=main,
                page = page,
                logged_in=authenticated_userid(request))
    

@view_config(route_name='why_create_user', renderer='templates/home.pt')
def WhyCreateUser(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='User').first()

    return dict(title='Why Create a User Account',
                main=main ,
                page = page,
                logged_in=authenticated_userid(request))
    
@view_config(route_name='new_user', renderer='templates/newuser.pt')
def CreateUser(request):
    main = get_renderer('templates/template.pt').implementation()
    if 'form.submitted' in request.params:
        new_user = Users('','','','','','','','','','','','','','','','','','','')
        new_user.username = request.params['username']
        new_user.password = request.params['password']
        new_user.firstname = request.params['firstname']
        new_user.middlename = request.params['middlename']
        new_user.lastname = request.params['lastname']
        new_user.birthday = datetime.date(int(request.params['year']),int(request.params['month']),int(request.params['day']))
        new_user.gender = request.params['gender']
        new_user.street = request.params['street']
        new_user.city = request.params['city']
        new_user.state = request.params['state']
        new_user.zipcode = request.params['zipcode']
        new_user.phonenumber = request.params['phonenumber']
        new_user.email = request.params['email']
        DBSession.add(new_user)
    
    return dict(title='Why Create a User Account',
                main=main ,
                logged_in=authenticated_userid(request))
    
@view_config(route_name='why_register_patient', renderer='templates/home.pt')
def WhyRegisterPatient(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='Patient').first()

    return dict(title='Why Register A Patient Account',
                main=main ,
                page = page,
                logged_in=authenticated_userid(request))
    
@view_config(route_name='why_register_medic', renderer='templates/home.pt')
def WhyRegisterMedic(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='Medic').first()

    return dict(title='Why Register A Medic Account',
                main=main ,
                page = page,
                logged_in=authenticated_userid(request))
    
@view_config(route_name='why_register_director', renderer='templates/home.pt')
def WhyRegisterDirector(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='Director').first()

    return dict(title='Why Register A Medical Director Account',
                main=main ,
                page = page,
                logged_in=authenticated_userid(request))
    
    
    
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
        if USERS.get(login) == password:
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
        logged_in=authenticated_userid(request))

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

