from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, WishlistItem
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.fields import ImageField

# Profile Serializer      
class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    role = serializers.ChoiceField(choices=Profile.Role.choices, default=Profile.Role.BUYER)
    class Meta:
        model = Profile
        fields = ['name', 'image', 'contact_info', 'shopping_preferences', 'role']


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.save()

        if profile_data:
            profile.name = profile_data.get('name', profile.name)
            #  if 'image' in profile_data:  # Only update if image is provided
            #     profile.image = profile_data.get('image', profile.image)
            profile.image = profile_data.get('image', profile.image)
            profile.contact_info = profile_data.get('contact_info', profile.contact_info)
            profile.shopping_preferences = profile_data.get('shopping_preferences', profile.shopping_preferences)
            profile.role = profile_data.get('role', profile.role)
            profile.save()

        return instance


# Signup Serializer
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        # Ensure passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        # Check for unique username and email
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists."})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email is already registered."})
        return data

    def create(self, validated_data):
        # Remove confirm_password before creating the user
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
# login serializer
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)

# reset-password serializer
class ResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        # Check if user exists
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"username": "User does not exist."})

        # Check if passwords match
        if new_password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        return attrs

    def save(self, **kwargs):
        username = self.validated_data['username']
        new_password = self.validated_data['new_password']

        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()

        return user

# wishlist item serializer
class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ['id', 'user', 'product']

