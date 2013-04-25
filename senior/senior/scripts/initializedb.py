import os
import sys
import transaction
import datetime


from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    Page,
    Base,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        #model = MyModel(name='one', value=1)
        #DBSession.add(model)
        model = Page(name='Home', 
                     data='This is the Home page.')
        DBSession.add(model)
        model = Page(name='About', 
                     data='This is the About Us page.')
        DBSession.add(model)
        model = Page(name='Contact', 
                     data='This is the Contact Us page.')
        DBSession.add(model)
        model = Page(name='User', 
                    data='This is the Why Should you Create a User Account Page.')
        DBSession.add(model)
        model = Page(name='Patient', 
                     data='This is the Why Should you Register as a Patient page.')
        DBSession.add(model)
        model = Page(name='Medic', 
                     data='This is the Why Should you Register as a Medic page.')
        DBSession.add(model)
        model = Page(name='Director', 
                     data='This is the Why Should you Register as a Medical Director page.')
        DBSession.add(model)
