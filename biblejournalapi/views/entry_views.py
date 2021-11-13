from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from biblejournalapi.models import Entry, Reader, reader
from django.contrib.auth.models import User
class EntryView(ViewSet):
    def retrieve(self,request, pk):
        entries = Entry.objects.get(pk=pk)
        seriailizer = EntrySerializer(entries, many=False, context={'request': request})
        return Response(seriailizer.data)
    def list(self, request):
        reader = Reader.objects.get(user = request.auth.user)
        entries = Entry.objects.filter(reader = reader)
        seriailizer = EntrySerializer(entries, many=True, context={'request': request})
        return Response(seriailizer.data)
    def create(self, request):
        reader = Reader.objects.get(user = request.auth.user)
        try:
            Entry.objects.create(
                hear = request.data['hear'],
                engage = request.data['engage'],
                apply = request.data['apply'],
                respond = request.data['respond'],
                date = request.data['date'],
                refrence = request.data['refrence'],
                reader = reader
            )
            return Response({'Request': "Entry Posted"}, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',)
class ReaderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Reader
        fields = ('user',)
class EntrySerializer(serializers.ModelSerializer):
    reader = ReaderSerializer()
    class Meta:
        model = Entry
        fields = ('reader', 'hear', 'engage', 'apply', 'respond', 'date', 'refrence',)