from logistics_project.apps.tanzania.tests.base import TanzaniaTestScriptBase
from logistics_project.apps.tanzania.tests.util import register_user, add_products
from logistics.models import Product, ProductStock
from logistics.util import config
from django.utils import translation
from django.utils.translation import ugettext as _

class TestLossesAdjustments(TanzaniaTestScriptBase):
        
    def setUp(self):
        super(TestLossesAdjustments, self).setUp()
        ProductStock.objects.all().delete()
        
    def testLossesAdjustments(self):
        translation.activate("sw")

        contact = register_user(self, "778", "someone")
        add_products(contact, ["id", "dp", "ip"])

        script = """
            778 > Hmk Id 400 Dp 569 Ip 678
            778 < %(soh_confirm)s
        """ % {"soh_confirm": _(config.Messages.SOH_CONFIRM)}
        self.runScript(script)

        self.runScript(script)
        self.assertEqual(3, ProductStock.objects.count())
        for ps in ProductStock.objects.all():
            self.assertEqual(contact.supply_point, ps.supply_point)
            self.assertTrue(0 != ps.quantity)
        
        script = """
            778 > um id -3 dp -5 ip 13
            778 < %(loss_adjust_confirm)s
        """ % {"loss_adjust_confirm": _(config.Messages.LOSS_ADJUST_CONFIRM)}
        self.runScript(script)

        self.assertEqual(397, ProductStock.objects.get(product__sms_code="id").quantity)
        self.assertEqual(564, ProductStock.objects.get(product__sms_code="dp").quantity)
        self.assertEqual(691, ProductStock.objects.get(product__sms_code="ip").quantity)

    def testLossesAdjustmentsLAKeyword(self):
        translation.activate("sw")

        contact = register_user(self, "778", "someone")
        add_products(contact, ["id", "dp", "ip"])

        script = """
            778 > Hmk Id 400 Dp 569 Ip 678
            778 < %(soh_confirm)s
        """ % {"soh_confirm": _(config.Messages.SOH_CONFIRM)}
        self.runScript(script)

        self.assertEqual(3, ProductStock.objects.count())
        for ps in ProductStock.objects.all():
            self.assertEqual(contact.supply_point, ps.supply_point)
            self.assertTrue(0 != ps.quantity)

        script = """
            778 > la id -3 dp -5 ip 13
            778 < %(loss_adjust_confirm)s
        """ % {"loss_adjust_confirm": _(config.Messages.LOSS_ADJUST_CONFIRM)}
        self.runScript(script)

        self.assertEqual(397, ProductStock.objects.get(product__sms_code="id").quantity)
        self.assertEqual(564, ProductStock.objects.get(product__sms_code="dp").quantity)
        self.assertEqual(691, ProductStock.objects.get(product__sms_code="ip").quantity)
