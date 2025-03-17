from django.urls import path,include
from . import views



urlpatterns = [

    path('',views.newmemberDashboard,name='newmemberDashboard'),

    path('activation/',views.Activation,name='activation'),
    
    # path('memberDashboard/',views.memberDashboard,name='memberDashboard'),
    path('changePassowrd/',views.changePassowrd,name='changePassowrd'),
    path('adcenter/',views.adCenter,name='adcenter'),
    path('adsTeam/',views.adsTeam,name='adsTeam'),
    path('directTeam/',views.directTeam,name='directTeam'),
    path('levelTeam/',views.levelTeam,name='levelTeam'),
    path('directBonus/',views.directBonus,name='directBonus'),
    path('levelBonus/',views.levelBonus,name='levelBonus'),
    path('adBonus/',views.adBonus,name='adBonus'),
    path('adsTeam/',views.adsTeam,name='adsTeam'),
    path('withdrawal/',views.withdrawal,name='withdrawal'),
    path('verify-transaction/', views.verify_transaction, name='verify_transaction'),
    path('get-busd-price/', views.get_busd_price, name='get_busd_price'),
    path('verifyTransaction/', views.verifyTransaction, name='verifyTransaction'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('walletHistory/', views.walletHistory, name='walletHistory'),
    path('activate-id/', views.activateMemberId, name='activateMemberId'),
    path('kycPage/',views.kycPage,name='kycPage'),
    path('preConfirmEmail/',views.preConfirmEmail,name='preConfirmEmail'),
    path('linkexpired/',views.linkExpired,name='linkexpired'),
    path('magicbonus/',views.magicbonus,name='magicbonus'),
    path('socialmedia/',views.socialmedia,name='socialmedia'),
    path('mail-confirm-page/',views.mailConfirmPage,name='mailConfirmPage'),
    path('coutdownkyc/',views.coutdownkyc,name='coutdownkyc'),
    path('groupcoutdownkyc/',views.groupcoutdownkyc,name='groupcoutdownkyc'),
    path('community/',views.community,name='community'),
    # path('activate/', views.activate_id, name='activate_id'),
    # path('ind/', views.ind, name='ind'),
    
    path('logout/', views.custom_logout, name='custom_logout'),
    path('rimberiowallet/',views.rimberiowallet,name='rimberiowallet'),
    path('makePayment/',views.makePayment,name='makePayment'),
    path('checkPayment/',views.checkPayment,name='checkPayment'),

   path('cpmleted-tasks', views.CompletedTasks, name="completed-tasks"),
   path('testWalletTopup/', views.testWalletTopup, name="testWalletTopup"),
   path('unconfirmedEmail/',views.unconfirmedEmail,name='unconfirmedEmail'),
   path('activate-member/',views.activateAnyMembersId,name='activateAnyMembersId'),
   path('topup-member-id/',views.topUpMemberId,name='topUpMemberId'),
   path('dummy-withdrawal/',views.dummyWitdrawal,name='dummyWitdrawal'),
   path('club-bonus/',views.clubBonus,name='clubBonus'),
   path('submittedSocialJobThroughLink/',views.submittedSocialJobThroughLink,name='submittedSocialJobThroughLink'),
   path('sendAssignedJobToUserMail/',views.sendAssignedJobToUserMail,name='sendAssignedJobToUserMail'),
   path('submit-social-job/<uidb64>/<asidb64>/<token>/', views.submit_social_job, name='submit_social_job'),
   # path('submit-social-job-new/<uidb64>/<asidb64>/<token>/', views.submit_social_job_new, name='submit_social_job_new'),
   path('sendMailToUser/', views.sendMailToUser, name='sendMailToUser'),
   path('userProfile/', views.userProfile, name='userProfile'),
   path('viewClubs/', views.viewClubs, name='viewClubs'),
   path('groupDashboard/', views.groupDashboard, name='groupDashboard'),
   path('fiterlevelincome', views.filter_level_bonus, name='fiterlevelincome'),
   path('fiterlevelTeam', views.fiterlevelTeam, name='fiterlevelTeam'),
   path('rimberiowalletsocialjobs', views.rimberiowalletsocialjobs, name='rimberiowalletsocialjobs'),
   path('rimberiowalletpackageactivation', views.rimberiowalletpackageactivation, name='rimberiowalletpackageactivation'),
   path('rimberiowalletlevel', views.rimberiowalletlevel, name='rimberiowalletlevel'),
   path('rimberiowalletsocialjobslevel', views.rimberiowalletsocialjobslevel, name='rimberiowalletsocialjobslevel'),
   path('bonusReport', views.bonusReport, name='bonusReport'),
   path('viewMagicBonusDetails/<str:memid>/', views.viewMagicBonusDetails, name='viewMagicBonusDetails'),
   path('NewActivation/', views.NewActivation, name='NewActivation'),
   path('peerActivationNew/', views.peerActivationNew, name='peerActivationNew'),
   path('connectwallet/', views.connectwallet, name='connectwallet'),
   path('groupwithdarwals/', views.groupwithdarwals, name='groupwithdarwals'),
   path('get-usdt-abi/', views.get_usdt_abi, name='get_usdt_abi'),
   path('spendRitcoins/', views.spendRitcoins, name='spendRitcoins'),
   path('redeemRitcoins/', views.redeemRitcoins, name='redeemRitcoins'),
   path('c', views.redeemCoins, name='redeemCoins'),
   path('depositFund', views.depositFund, name='depositFund'),
   path('addWalletAddress/', views.addWalletAddress, name='addWalletAddress'),

  
]


htmx_urlpatterns=[
   path('sendSocialJob/',views.sendSocialJob,name='sendSocialJob'),
    
]

urlpatterns+=htmx_urlpatterns


