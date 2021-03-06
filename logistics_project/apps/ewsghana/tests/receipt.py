from rapidsms.tests.scripted import TestScript
from rapidsms.contrib.messagelog.models import Message
from logistics.models import Location, SupplyPointType
from logistics.models import SupplyPoint as Facility
from logistics_project.apps.ewsghana import app as logistics_app

class TestReceipts (TestScript):
    apps = ([logistics_app.App])
    fixtures = ["ghana_initial_data.json"] 
    def setUp(self):
        TestScript.setUp(self)
        location = Location.objects.get(code='de')
        facilitytype = SupplyPointType.objects.get(code='hc')
        rms = Facility.objects.get(code='garms')
        facility = Facility(code='dedh', name='Dangme East District Hospital',
                       location=location, active=True,
                       type=facilitytype, supplied_by=rms)
        facility.save()

    def testReceipt(self):
        a = """
           16176023315 > register stella dedh
           16176023315 < Congratulations stella, you have successfully been registered for the Early Warning System. Your facility is Dangme East District Hospital
           16176023315 > rec jd 10
           16176023315 < Thank you, you reported receipts for jd.
           16176023315 > rec jd 10 mc 20
           16176023315 < Thank you, you reported receipts for jd mc.
           """
        self.runScript(a)

