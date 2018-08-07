from django.contrib.auth.models import User, Group
from rest_framework import serializers
from quickstart.models import AnnotatedRecording, DemographicInformation

class AnnotatedRecordingSerializer(serializers.ModelSerializer):
  class Meta():
    model = AnnotatedRecording
    fields = ('file', 'hash_string', 'surah_num', 'ayah_num', 'timestamp', 'session_id')

class DemographicInformationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
        model = DemographicInformation
        fields = ('session_id', 'platform', 'gender', 'age', 'ethnicity', 'country', 'timestamp')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
