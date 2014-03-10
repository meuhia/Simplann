from datetime import datetime
import factory
from factory.compat import UTC
from factory.fuzzy import FuzzyDateTime

from Simplan.event.models import OptionTime, OptionFree, MakeChoice, \
    MakeGuestChoice, MakeUserChoice, EventUser, EventGuest, Choice


class OptionTimeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = OptionTime
    
    start_date = datetime(2014, 1, 1)

class OptionFreeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = OptionFree
        
    text = factory.Sequence(lambda n: 'Option{0}'.format(n))

class MakeChoiceFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MakeChoice

class MakeGuestChoiceFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MakeGuestChoice

class MakeUserChoiceFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MakeUserChoice

class ChoiceFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Choice
    
    title = factory.Sequence(lambda n: 'choix{0}'.format(n))
    description = factory.Sequence(lambda n: 'courte description du choix{0}'.format(n))
    positive = factory.Iterator([True, False])

class EventUserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = EventUser
    
    title = factory.Sequence(lambda n: u'Mon Evenement No{0}'.format(n))
    description = factory.Sequence(lambda n: 'La mini description de mon Evenement No{0}'.format(n))
    place = factory.Iterator(['Paris', 'Geneve', 'Kiev', 'Londres', None])
    mailing_list = 'destinator1@gmail.com, destinator2@gmail.com'
    
class EventGuestFactory(factory.DjangoModelFactory):
    FACTORY_FOR = EventGuest
    
    title = factory.Sequence(lambda n: 'Mon Evenement No{0}'.format(n))
    description = factory.Sequence(lambda n: 'La mini description de mon Evenement No{0}'.format(n))
    place = factory.Iterator(['Paris', 'Geneve', 'Kiev', 'Londres', None])
    author = factory.Sequence(lambda n: 'Auteur{0}'.format(n))
    email = factory.Sequence(lambda n: 'author{0}@gmail.com'.format(n))
    mailing_list = 'destinator1@gmail.com, destinator2@gmail.com'
    
