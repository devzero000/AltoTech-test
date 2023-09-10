import os

from django.conf import settings
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.indexes import VectorstoreIndexCreator
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ActionRelatedSerializerMixin(object):
    """
    Overrides get_serializer_class to choose the read serializer
    for GET requests and the write serializer for POST requests.

    Flow:  (`-->` = `fallback`)
    CREATE: `create_serializer_class` --> `write_serializer_class`
    UPDATE: `update_serializer_class` --> `write_serializer_class`
    LIST: `list_serializer_class`
    RETRIEVE: `retrieve_serializer_class` --> `list_serializer_class`

    ref: https://www.revsys.com/tidbits/using-different-read-and-write-serializers-django-rest-framework/
    """

    list_serializer_class = None
    retrieve_serializer_class = None

    write_serializer_class = None
    create_serializer_class = None
    update_serializer_class = None

    def get_serializer_class(self):
        if self.action in ['create']:
            return self.get_create_serializer_class()
        if self.action in ['update', 'partial_update']:
            return self.get_update_serializer_class()
        if self.action in ['retrieve']:
            return self.get_retrieve_serializer_class()
        return self.get_list_serializer_class()

    def get_list_serializer_class(self):
        assert self.list_serializer_class is not None, (
            f'\'{self.__class__.__name__}\' should either include a `list_serializer_class` attribute,'
            'or override the `get_list_serializer_class()` method.'
        )
        return self.list_serializer_class

    def get_retrieve_serializer_class(self):
        return self.retrieve_serializer_class or self.get_list_serializer_class()

    def get_write_serializer_class(self):
        assert self.write_serializer_class is not None, (
            f'\'{self.__class__.__name__}\' should either include a `write_serializer_class` attribute,'
            'or override the `get_write_serializer_class()` method.'
        )
        return self.write_serializer_class

    def get_create_serializer_class(self):
        return self.create_serializer_class or self.get_write_serializer_class()

    def get_update_serializer_class(self):
        return self.update_serializer_class or self.get_write_serializer_class()


class ChatGPTView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        question = request.data.get('question', '')
        if not question:
            raise ValueError('Please enter question.')

        os.environ["OPENAI_API_KEY"] = settings.TOKEN_OPENAI
        loader = DirectoryLoader('main/data/')
        index = VectorstoreIndexCreator().from_loaders([loader])
        response = index.query(question).strip()
        return Response(data={'message': response})
