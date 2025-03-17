from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import ZqUser
from django import forms
from django.contrib.auth.forms import PasswordChangeForm

# from django import forms
from django.core.exceptions import ValidationError
from .models import SubmittedDataForSocialMedia
import os
from django.utils import timezone

class UserForm(UserCreationForm):
    
    email = forms.EmailField(required=True)
    introducerid = forms.CharField(required=False)

    class Meta:
        model = ZqUser
        fields = ['username','email','introducerid','password1','country','local_currency','state','phone_number']
        
  
    # def clean_username(self):
    #     username = self.cleaned_data.get("username")
        
    #     if len(username)>8:
    #          raise forms.ValidationError("username  can not contain more than 8 characters") 
              
    def clean_password2(self):
        
        # print("came to clean password in zqUsers")
        password1 = self.cleaned_data.get("password1")
        confirm_password = self.cleaned_data.get("password2")

        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return confirm_password
    
    # def clean_plain_password(self):
        
    #     # print("came to clean password in zqUsers")
    #     password1 = self.cleaned_data.get("password1")
    #     confirm_password = self.cleaned_data.get("password2")

    #     if password1 and confirm_password and password1 != confirm_password:
    #         raise forms.ValidationError("Passwords do not match")

    #     return confirm_password
        
        
        
    def clean_introducerid(self):
        
        # print("came to clean introducerid in zqUsers")
        compInfo=ZqUser.objects.get(id=1)
        introid = self.cleaned_data.get("introducerid")
        print("came to clean introducer id")

        if introid!='':
            
            try:
                if introid.strip().lower().startswith('rb') or introid.strip().lower().startswith('rb'):
                    introducerid = ZqUser.objects.get(memberid=introid)
                    
                    print(introducerid)
                    
                else:
                    introducerid = ZqUser.objects.get(username=introid)
                    print(introducerid)
                # print(introducerid)
                return introducerid
            except ZqUser.DoesNotExist:
                raise forms.ValidationError("Introducer with the specified member ID does not exist.")
            
        else:
            return compInfo
            


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if ZqUser.objects.filter(email=email).exists():
            raise ValidationError('A user with this email address already exists.')
        return email

    def save(self, commit=True):
        
        user = super().save(commit=False)
        user.plain_password = self.cleaned_data["password1"]
        if commit:
            user.save()
        return user
      
    
    
   
class OTPVerificationForm(forms.Form):
    otp = forms.CharField(required=True)

    def clean_otp(self):
        otp = self.cleaned_data.get('otp')
       
        # Add your OTP validation logic here
        if not otp.isdigit() or len(otp) != 6:
            raise forms.ValidationError('Invalid OTP. Please enter a 6-digit number.')
         # Check if the provided OTP matches the one stored in the session
        stored_otp = self.request.session.get('OTP')  # Assuming 'otp' is the key used to store OTP in session
        if str(otp) != str(stored_otp):
            raise forms.ValidationError('Incorrect OTP. Please enter the correct OTP.')
        
        return otp
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Get request object
        super().__init__(*args, **kwargs)
    
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    
    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        
        # Check if there are multiple accounts with the same email
        if ZqUser.objects.filter(email=email).count() > 1:
            raise forms.ValidationError("Multiple accounts exist with this email. Please login through username.")


        return cleaned_data
    

class ChangePasswordForm(forms.Form):
    password = forms.CharField(required=True)
    enterNewPasssord = forms.CharField(required=True)
    confirmPassword = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("enterNewPasssord")
        confirm_password = cleaned_data.get("confirmPassword")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")

        return cleaned_data
    


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Current Password'}),
        label='Current Password'
    )
    
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your New Password'}),
        label='New Password'
    )
    
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Your New Password'}),
        label='Confirm Password'
    )
    
    


class SubmittedDataForSocialMediaForm(forms.ModelForm):
    class Meta:
        model = SubmittedDataForSocialMedia
        fields = [
           
            'twitter_image', 'insta_image', 'youtube_image', 
             
        ]

    # def clean_greview_image(self):
    #     return self.validate_image(self.cleaned_data.get('greview_image'))

    # def clean_facebook_image(self):
    #     return self.validate_image(self.cleaned_data.get('facebook_image'))

    def clean_twitter_image(self):
        return self.validate_image(self.cleaned_data.get('twitter_image'))

    def clean_insta_image(self):
        return self.validate_image(self.cleaned_data.get('insta_image'))

    def clean_youtube_image(self):
        return self.validate_image(self.cleaned_data.get('youtube_image'))

    def validate_image(self, image):
        if image:
            ext = os.path.splitext(image.name)[1]
            valid_extensions = ['.jpg', '.jpeg', '.png']
            if ext.lower() not in valid_extensions:
                raise ValidationError('Unsupported file extension.')
            
            # File size validation (e.g., max 5MB)
            if image.size > 2 * 1024 * 1024:
                raise ValidationError('File size exceeds 2MB.')
        return image
    
    def save(self, commit=True, request=None):
            instance = super().save(commit=False)
            if request and request.user.is_authenticated:
                instance.uploadedby = request.user
            if commit:
                instance.save()
            return instance
