from django.urls import path,include
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('',views.index,name='index'),
    path('index/',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('accounts/login/',views.userLogin,name='login'),
    path('register-success/',views.success,name='success'),
    path('authenticate/',views.otpVerify,name='authenticate'),
    path('password-reset/',views.resetPassword,name='passwordReset'),
    path('reset-otp-verify/',views.resetOtpVerify,name='resetOtpVerify'),
    path('new-password/',views.newPassword,name='newPassword'),
    path('resend-otp/',views.resendOTPResetPass,name='resendOTP'),
    path('resend-otp-registration/',views.resendOTPReg,name='resendOTPReg'),
    path('test-it-out/',views.testitout,name='testitout'),
    path('get_member_name/',views.returnMemberName,name='returnMemberName'),
    path('token/',views.token,name='token'),
    path('termsCondition/',views.termsCondition,name='termsCondition'),
    path('roadmap/',views.roadmap,name='roadmap'),
    path('mining/',views.mining,name='mining'),
    path('about/',views.about,name='about'),
   
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('resetPassConf/<uidb64>/<token>/', views.resetPassConf, name='resetPassConf'),
    path('email_verification_sent/', TemplateView.as_view(template_name="email_verification_sent.html"), name='email_verification_sent'),
    path('changepass/', views.changePassword, name='changePassword'),
    path('resetpass/', views.resetPass, name='resetPass'),
    path('mainConfirm/', views.mainConfirm, name='mainConfirm'),
    path('confirm-email/',views.confirmEmail,name='confirmEmail'),
    path('resendactivationemail/',views.resendActivationEmail,name='resendActivationEmail'),
    path('sendtestmail/',views.sendtestmail,name='sendtestmail'),



    # path('calculate-roi/',views.calculateROI,name='calculateROI'),
    # path('getcbaddress/',views.getAddress,name='getAdd'),
    
   
]



