from rest_framework import serializers,validators
from django.contrib.auth.password_validation import validate_password
from profiles.models import CustomUser, Profile

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[validators.UniqueValidator(queryset=CustomUser.objects.all())]) #aynı email ile kayıt olamasın
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password]) # validators=[validate_password()] settinf py dosyasındaki sifre dofrulama tekniklerini uygulaması içi yazdık
    
    
    class Meta:
        model = CustomUser
        fields = ('id','username','password','email') #id readonly dir
        
    def create(self,validated_data):
        user = CustomUser.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        ) #create yerine create_user kullandık ki passwordu hashleyerek yazsın
        
        return user
    

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ('id','username')
        

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ('id','user')