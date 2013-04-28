from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from senior.security import (
    groupfinder,
    get_user,
    )


from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    authn_policy = AuthTktAuthenticationPolicy('sosecret', callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings, root_factory='senior.models.RootFactory')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_request_method(get_user, 'user', reify=True)

    
    config.add_route('home', '/')
    config.add_route('about_us','/about_us')
    config.add_route('contact_us','/contact_us')
    
    config.add_route('why_create_user','/why_create_user')
    config.add_route('new_user','/new_user')
    config.add_route('edit_user','/edit_user')
    config.add_route('view_user','/view_user')
                     
    config.add_route('why_register_patient','/why_register_patient')
    config.add_route('register_patient','/register_patient')
    config.add_route('edit_patient','/edit_patient')
    config.add_route('view_patient','/view_patient')
    config.add_route('patient_history','/patient_history')
                     
    config.add_route('why_register_medic','/why_register_medic')
    config.add_route('register_medic','/register_medic')
    config.add_route('edit_medic','/edit_medic')
    config.add_route('view_medic','/view_medic')
    config.add_route('view_patient_as_medic','/view_patient_as_medic')
    config.add_route('medic_history','/medic_history')
                     
    config.add_route('why_register_director','/why_register_director')
    config.add_route('register_director','/register_director')
    config.add_route('edit_director','/edit_director')
    config.add_route('view_director','/view_director')
    config.add_route('view_patient_as_director','/view_patient_as_director')
    config.add_route('view_patient_history','/view_patient_history')
    config.add_route('view_medic_as_director','/view_medic_as_director')
    config.add_route('view_medic_history','/view_medic_history')
                     
    config.add_route('admin_edit_user','/admin_edit_user')
    config.add_route('admin_edit_patient','/admin_edit_patient')
    config.add_route('admin_edit_medic','/admin_edit_medic')
    config.add_route('admin_edit_director','/admin_edit_director')
    config.add_route('view_all_users','/view_all_users')
    config.add_route('view_all_patients','/view_all_patients')
    config.add_route('view_all_medics','/view_all_medics')
    config.add_route('view_all_directors','/view_all_directors')


    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.scan()
    return config.make_wsgi_app()
