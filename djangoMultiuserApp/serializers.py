from .models import UserAccount, Doctor, Patient
from rest_framework import serializers



class DoctorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['email','password','role']
        extra_kwargs={
            'password':{'write_only':True}
        }

        def create(self,validate_data):
            return Doctor.objects.create_user(**validate_data)
    
class PatientRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['email','password','role']
        extra_kwargs={
            'password':{'write_only':True}
        }

        def create(self,validate_data):
            print(validate_data)
            return Patient.objects.create_user(**validate_data)
        

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id','email','role']

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = UserAccount
        fields = ['email','password']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm password does not match")
        user.set_password(password)
        user.save()
        return attrs