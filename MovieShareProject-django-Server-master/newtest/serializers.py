from rest_framework import serializers
from .models import *


class ClientSerializer(serializers.ModelSerializer):

    class Meta:

        model = Client

        fields = ('clientid','password','pub_date',)


class PassIdSerializer(serializers.ModelSerializer):

	class Meta:

		model = PassId

		fields = ('id',)
