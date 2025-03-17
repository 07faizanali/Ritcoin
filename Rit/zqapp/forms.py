from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from zqUsers.models import ZqUser
from django import forms

class UserForm(UserCreationForm):
    
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    introducerid = forms.CharField(required=False)

    class Meta:
        model = ZqUser
        # fields = ['username','email','introducerid','password1']
        fields = ['username','email','introducerid','password1','country','local_currency','state','phone_number']
        
    


    def clean_username(self):
        print("came to clean username in zqapp")
        username = self.cleaned_data.get("username")
        
        if len(username)>8:
             raise forms.ValidationError("username  can not contain more than 8 characters")
              
    def clean_password2(self):
        print("came to clean password in zqapp")
        password1 = self.cleaned_data.get("password1")
        confirm_password = self.cleaned_data.get("password2")

        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return confirm_password
        
        
        
    def clean_introducerid(self):
        print("came to clean introid in zqapp")
        compInfo=ZqUser.objects.get(id=1)
        introid = self.cleaned_data.get("introducerid")

        if introid!='':
            
            try:
                introducerid = ZqUser.objects.get(username=str(introid).strip())
                # print(introducerid)
                return introducerid
            except ZqUser.DoesNotExist:
                raise forms.ValidationError("Introducer with the specified member ID does not exist.")
            
        else:
            return compInfo
            

    def save(self, commit=True):
        
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
 
   
class OTPVerificationForm(forms.Form):
    otp = forms.CharField(required=True)
    # email = forms.CharField(required=True)

    def clean_otp(self):
        # print('came here======')
        otp = self.cleaned_data.get('otp')
       
        # Add your OTP validation logic here
        if not otp.isdigit() or len(otp) != 6:
            raise forms.ValidationError('Invalid OTP. Please enter a 6-digit number.')
         # Check if the provided OTP matches the one stored in the session
        stored_otp = self.request.session.get('RegOTP')  # Assuming 'otp' is the key used to store OTP in session
        # print(stored_otp)
        if str(otp) != str(stored_otp):
            raise forms.ValidationError('Incorrect OTP. Please enter the correct OTP.')
        
        return otp
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Get request object
        super().__init__(*args, **kwargs)
    
# class LoginForm(forms.Form):
    #     email = forms.EmailField()
    #     password = forms.CharField(widget=forms.PasswordInput)
        
    #     def clean(self):
    #         cleaned_data = super().clean()
    #         email = cleaned_data.get("email")
            
    #         # Check if there are multiple accounts with the same email
    #         if ZqUser.objects.filter(email=email).count() > 1:
    #             raise forms.ValidationError("Multiple accounts exist with this email. Please login through username")

    #         return cleaned_data


class LoginForm(forms.Form):
    email_or_username = forms.CharField(max_length=150, label="Email or Username")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email_or_username = cleaned_data.get("email_or_username")
        password = cleaned_data.get("password")

        # Check if the input is an email
        if '@'  in email_or_username and  '.' in email_or_username:
            cleaned_data['email'] = email_or_username
            try:
                               
                if ZqUser.objects.filter(email=email_or_username).count() > 1:
                    raise forms.ValidationError("Multiple accounts exist with this email. Please login through username")
                else:
                    user = ZqUser.objects.get(email=email_or_username)
            except ZqUser.DoesNotExist:
                raise forms.ValidationError("User with this email does not exist.")
        # If it's not an email, assume it's a username
        else:
            cleaned_data['username'] = email_or_username
            try:
                # print('came here')
                user = ZqUser.objects.get(username=email_or_username)
                
            except ZqUser.DoesNotExist:
                raise forms.ValidationError("User with this username does not exist.")

        # Check if password is correct
        # print(user.check_password(password))
        if user and not user.check_password(password):
            # print(password)
            # print(user.check_password(password))
            # print(user)
            raise forms.ValidationError("Invalid password.")

        return cleaned_data
   

class ChangePasswordForm(forms.Form):
    password = forms.CharField(required=True)
    enterNewPasssord = forms.CharField(required=True)
    confirmPassword = forms.CharField(required=True)
    # email = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("enterNewPasssord")
        confirm_password = cleaned_data.get("confirmPassword")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")

        return cleaned_data
    
    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)  # Get request object
    #     super().__init__(*args, **kwargs)


class NewPasswordForm(forms.Form):
    
    password = forms.CharField(required=True)
    confPassword = forms.CharField(required=True)
    email = forms.CharField()
    
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confPassword")
        email = cleaned_data.get("email")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")

        return cleaned_data
    

    # def clean_otp(self):
    #     otp = self.cleaned_data.get('otp')
       
    #     # Add your OTP validation logic here
    #     if not otp.isdigit() or len(otp) != 6:
    #         raise forms.ValidationError('Invalid OTP. Please enter a 6-digit number.')
    #      # Check if the provided OTP matches the one stored in the session
    #     stored_otp = self.request.session.get('OTP')  # Assuming 'otp' is the key used to store OTP in session
    #     if str(otp) != str(stored_otp):
    #         raise forms.ValidationError('Incorrect OTP. Please enter the correct OTP.')
        
    #     return otp
        
    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)  # Get request object
    #     super().__init__(*args, **kwargs)
    