from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from rapidsms.contrib.handlers.handlers.tagging import TaggingHandler
from django.utils.translation import ugettext_noop as _
import re
from logistics.util import config
from logistics_project.apps.tanzania.models import SupplyPointStatus,\
    SupplyPointStatusTypes, SupplyPointStatusValues
from logistics.decorators import logistics_contact_required
        
class Supervision(KeywordHandler,TaggingHandler):
    """
    Supervision handler for responses to supervision inquiries
    """

    keyword = "supervision|usimamizi"    

    def help(self):        
        self.respond(_(config.Messages.SUPERVISION_HELP))
    
    @logistics_contact_required()
    def handle(self, text):
        sub_command = text.strip().lower()
        if re.match("hap", sub_command) or re.match("no", sub_command):
            SupplyPointStatus.objects.create\
                (status_type=SupplyPointStatusTypes.SUPERVISION_FACILITY,
                 status_value=SupplyPointStatusValues.NOT_RECEIVED,
                 supply_point=self.msg.logistics_contact.supply_point,
                 status_date=self.msg.timestamp)
            self.respond(_(config.Messages.SUPERVISION_CONFIRM_NO))
        elif re.match("ndi", sub_command) or re.match("yes", sub_command):
            SupplyPointStatus.objects.create\
                (status_type=SupplyPointStatusTypes.SUPERVISION_FACILITY,
                 status_value=SupplyPointStatusValues.RECEIVED,
                 supply_point=self.msg.logistics_contact.supply_point,
                 status_date=self.msg.timestamp)
            self.respond(_(config.Messages.SUPERVISION_CONFIRM_YES))
        else:
            self.add_tag("Error")
            self.help()
