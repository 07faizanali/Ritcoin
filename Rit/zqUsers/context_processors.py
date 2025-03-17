from wallet.models import CustomCoinRate
from zqUsers.models import ROIRates


def getZQLRate(request):


    # updatedZaanRate=CustomCoinRate.objects.order_by('-id').first().amount
    updatedZaanRate=float(CustomCoinRate.objects.filter(coin_name='ZQL').order_by('-id').first().amount)
    USDRate=float(CustomCoinRate.objects.filter(coin_name='USD').order_by('-id').first().amount)
    latestROIRate=int(ROIRates.objects.latest('set_date').rate)
    return {'ZQLRate':  updatedZaanRate,'LatestROIRate':latestROIRate,'USDRate':  USDRate}

def getZQLRateIn(request):


    # updatedZaanRate=CustomCoinRate.objects.order_by('-id').first().amount
    updatedZaanRate=float(CustomCoinRate.objects.filter(coin_name='ZQL').order_by('-id').first().amount)
    return {'ZQLRate':  updatedZaanRate}
def getLatestROIRate(request):


    # updatedZaanRate=CustomCoinRate.objects.order_by('-id').first().amount
    updatedZaanRate=float(CustomCoinRate.objects.filter(coin_name='ZQL').order_by('-id').first().amount)
    return {'ZQLRate':  updatedZaanRate}








