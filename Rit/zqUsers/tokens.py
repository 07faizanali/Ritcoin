# tokens.py
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

from .models import ZqUser,AssignedSocialJob

from django.utils.crypto import constant_time_compare

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)+six.text_type(user.joindate)+six.text_type(user.password)
        )
        
        
    # def check_token(self, user,asid, token):
    #     # Retrieve the token associated with the user
    #     stored_token = getattr(user, 'email_verification_token', None)
        
    #     # if 
    #     isTokenvalid=AssignedSocialJob.objects.get(id=asid)
        
    #     if not isTokenvalid:
    #         return False

    #     # Check if the stored token matches the token provided
    #     if stored_token and constant_time_compare(stored_token, token):
    #         # Mark the token as used (invalidate it)
    #         user.email_verification_token = None  # or mark it as used in another way
    #         user.save()
    #         return True
    #     return False

email_verification_token = EmailVerificationTokenGenerator()



