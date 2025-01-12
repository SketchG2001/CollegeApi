from rest_framework import serializers
from .models import CustomUser,States


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'mobile')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            mobile=validated_data.get('mobile', '')
        )
        return user



class StateFilterSerializer(serializers.Serializer):
    state = serializers.ChoiceField(choices=States.stateChoice)

    class Meta:
        model = States
        fields = ('state',)

    def get_choices(self):
        # Return the state choices in a format suitable for your frontend dropdown
        return self.fields['state'].choices





