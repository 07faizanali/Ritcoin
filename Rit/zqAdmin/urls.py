from django.urls import path,include
from . import views


urlpatterns = [

    path('dashboard/',views.adminDashboard,name='zqAdminDashboard'),
    path('distribute-mining/',views.distributeMining,name='distributeMining'),
    path('set-coin-rate/',views.setCoinRate,name='setCoinRate'),
    path('logout/',views.adminLogout,name='adminlogout'),
    # path('get-all-withdrawls/',views.allWithdrawls,name='allWithdrawls'),
    path('usdWithdrawls/',views.usdWithdrawls,name='usdWithdrawls'),
    path('adminwithdrawls/',views.adminwithdrawls,name='adminwithdrawls'),
    # path('get-approved-withdrawls/',views.approvedWithdrawls,name='approvedWithdrawals'),
    path('inrWithdrawls/',views.inrWithdrawls,name='inrWithdrawls'),
    path('verifyhelp/',views.verifyhelp,name='verifyhelp'),
    path('verifyhelpUSDT/',views.verifyhelpUSDT,name='verifyhelpUSDT'),
    path('verifyDeposits/',views.verifyDeposits,name='verifyDeposits'),
    path('cancel-withdrawl/',views.cancelWithdrawl,name='cancelWithdrawl'),
    path('activate-member-id/',views.activateIdOfAMember,name='activateIdOfAMember'),
    path('sendOTPToActivateId/',views.sendOTPToActivateId,name='sendOTPToActivateId'),
    path('viewAllMembers/',views.viewAllMembers,name='viewAllMembers'),
    # path('topupUserWallet/',views.topupUserWallet,name='topupUserWallet'),
    path('sendOTPToDepositInWallet/',views.sendOTPToDepositInWallet,name='sendOTPToDepositInWallet'),
    path('addFundsToMembersWallet/',views.addFundsToMembersWallet,name='addFundsToMembersWallet'),
    path('allInvestments/',views.allInvestments,name='allInvestments'),
    path('withdrawal-type/',views.WithdrawalType,name='withdrawal-type'),
     path('save-data/', views.Save_data, name='save_data'),
    path('allMembersROIs/',views.allMembersROIs,name='allMembersROIs'),
    path('allLatestDistributedROI/',views.allLatestDistributedROI,name='allLatestDistributedROI'),
    path('adminMemLogin/',views.adminMemLogin,name='adminMemLogin'),
    path('kycimages/',views.kycimages,name='kycimages'),
    path('makeTrans/',views.makeTrans,name='makeTrans'),
    path('verifysocialjobdata/',views.verifysocialjobdata,name='verifysocialjobdata'),


    path('cancelWithdrawl/',views.cancelWithdrawl,name='cancelWithdrawl'),
    path('addsocialjob/',views.addsocialjob,name='addsocialjob'),
    path('club-1-members/',views.club1members,name='club1members'),
    path('club-2-members/',views.club2members,name='club2members'),
    path('club-3-members/',views.club3members,name='club3members'),
    path('club-members-income/<int:clubid>/',views.ClubMembersIncomes,name='ClubMembersIncomes'),
    path('distributeIncomeToClubMembers/',views.distributeIncomeToClubMembers,name='distributeIncomeToClubMembers'),
    path('addMembersToClub/',views.addMembersToClub,name='addMembersToClub'),
    path('memberWalletwithdraw/',views.memberWalletwithdraw,name='memberWalletwithdraw'),
    path('blockMember/',views.blockMember,name='blockMember'),
    path('blockMemberWithdrawal/',views.blockMemberWithdrawal,name='blockMemberWithdrawal'),


    path('', views.Questions, name="questions"),
    path('changeMemberPassword/', views.changeMemberPassword, name="changeMemberPassword"),
    path('meminfodata/', views.data_view, name='meminfodata'),
    path('allMemsInfo/', views.allMemsInfo, name='allMemsInfo'),
    path('data/<str:data_type>/', views.paginated_table_data_view, name='paginated_table_data'),
    path('paginated_table_data/', views.paginated_table_data, name='paginated_table_data_real'),
    path('unblockMemberWithdrawal/', views.unblockMemberWithdrawal, name='unblockMemberWithdrawal'),
    path('search-member-username/', views.search_member_username, name='search_member_username'),
    path('manageRitcoinsRedemption/', views.manageRitcoinsRedemption, name='manageRitcoinsRedemption'),



]




