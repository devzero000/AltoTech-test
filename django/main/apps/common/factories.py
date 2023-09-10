import factory


class ModelControllerFactory(factory.django.DjangoModelFactory):
    created_user = factory.SubFactory('main.apps.users.factories.UserFactory')
    updated_user = factory.SelfAttribute('created_user')
