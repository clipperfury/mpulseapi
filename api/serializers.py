from rest_framework import serializers
from api.models import Member
from api.models import File
from rest_framework.validators import UniqueTogetherValidator


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'client_member_id', 'account_id','created']

        validators = [
            UniqueTogetherValidator(
                queryset=Member.objects.all(),
                fields=['account_id', 'phone_number']
            ),
            UniqueTogetherValidator(
                queryset=Member.objects.all(),
                fields=['client_member_id', 'phone_number']
            )
        ]

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"
