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
    Base,
    Page,
    User,
    Patient,
    Medic,
    Director,
    Allergy,
    MedicalHistory,
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
        #Initialize all of the pages content
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
        ''' This is a template of a new user.
        model = User( login = '',
                      password = '',
                      first_name = '',
                      middle_name = '',
                      last_name = '',
                      gender = '',
                      birthday = datetime.date(),
                      primary_language = '',
                      secondary_language = '',
                      social_security =  ,
                      phone = '',
                      street = '',
                      city = '',
                      state = '',
                      zipcode = '',
                      email = ''
                      )
        DBSession.add(model)
        '''
        model = User( login = 'turdona193',
                      password = 'nick',
                      first_name = 'Nicholas',
                      middle_name = 'Anthony',
                      last_name = 'Turdo',
                      gender = 'Male',
                      birthday = datetime.date(1991,1,26),
                      primary_language = 'English',
                      secondary_language = 'None',
                      social_security =  000000000,
                      phone = '0000000000',
                      street = '3510 Barrington Dr.',
                      city = 'Potsdam',
                      state = 'NY',
                      zipcode = '13676',
                      email = 'turdona193@potsdam.edu'
                      )
        DBSession.add(model)
        
        model = User( login = 'samsonm324',
                      password = 'mike',
                      first_name = 'Mike',
                      middle_name = '',
                      last_name = 'Samson',
                      gender = 'Male',
                      birthday = datetime.date(1989,2,23),
                      primary_language = 'English',
                      secondary_language = 'None',
                      social_security =  000000000,
                      phone = '0000000000',
                      street = '234 Pine Str.',
                      city = 'Potsdam',
                      state = 'NY',
                      zipcode = '13676',
                      email = 'samsonm324@somewhere.edu'

                      )
        DBSession.add(model)

        model = User( login = 'smithjp198',
                      password = 'john',
                      first_name = 'John',
                      middle_name = 'Paul',
                      last_name = 'Smith',
                      gender = 'Male',
                      birthday = datetime.date(1992,4,6),
                      primary_language = 'English',
                      secondary_language = 'French',
                      social_security =  000000000,
                      phone = '0000000000',
                      street = '26 State Str.',
                      city = 'Potsdam',
                      state = 'NY',
                      zipcode = '13676',
                      email = 'smithjp198@somewhere.edu'

                      )
        DBSession.add(model)
        
        model = User( login = 'paulfj123',
                      password = 'frank',
                      first_name = 'Frank',
                      middle_name = 'John',
                      last_name = 'Paul',
                      gender = 'Male',
                      birthday = datetime.date(1973,2,3),
                      primary_language = 'Spanish',
                      secondary_language = 'English',
                      social_security =  000000000,
                      phone = '0000000000',
                      street = '423 SpringField.',
                      city = 'Potsdam',
                      state = 'NY',
                      zipcode = '13676',
                      email = 'paulfj123@somewhere.edu'
                      )
        DBSession.add(model)
        '''
        model = Patient(user = '',
                        primary_physician = ''
                        )
        '''
        model = Patient(user = 'turdona193',
                        rfidtag = "0001",
                        primary_physician = 'Dr.Moose'
                        )
        DBSession.add(model)

        model = Patient(user = 'paulfj123',
                        rfidtag = "0002",
                        primary_physician = 'Dr.Doctor'
                        )
        DBSession.add(model)
        '''
        model = Allergy(user = '',
                        allergy = ''
                        )
        '''
        model = Allergy(user = 'turdona193',
                        allergy = 'Bees'
                        )
        DBSession.add(model)
        model = Allergy(user = 'paulfj123',
                        allergy = 'cotton'
                        )
        DBSession.add(model)

        '''
        model = MedicalHistory(user = '',
                              event = ''
                              )
        '''
        model = MedicalHistory(user = 'turdona193',
                              event = 'Broken leg on January First, 2001'
                              )
        DBSession.add(model)
        
        '''
        model = Medic(user = '',
                      training_level = '',
                      cert_number = ''
                      )
        '''
        model = Medic(user = 'turdona193',
                      training_level = 'EMT-Basic',
                      cert_number = '389992'
                      )
        DBSession.add(model)
        model = Medic(user = 'smithjp198',
                      training_level = 'EMT-Basic',
                      cert_number = '342234'
                      )
        DBSession.add(model)
        '''
        model = Director(user = ''
                                )
        '''
        model = Director(user = 'samsonm324'
                                )
        DBSession.add(model)



        
