from django.contrib.auth.models import User
import factory

from Simplan.account.models import Profile


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    
    username = factory.Sequence(lambda n: 'jondoe{0}'.format(n))
    email = factory.Sequence(lambda n: 'babardechine{0}@gmail.com'.format(n))
    password = '1234'
    is_active = True
    
    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user
    
class ProfileFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Profile
    
    id_facebook = factory.LazyAttribute(lambda a:'{0}-{1}'.format(a.user.username.lower(), 'fb'))
    id_twitter = factory.LazyAttribute(lambda a:'{0}-{1}'.format(a.user.username.lower(), 'twitter'))
    id_gplus = factory.LazyAttribute(lambda a:'{0}-{1}'.format(a.user.username.lower(), 'gplus'))
