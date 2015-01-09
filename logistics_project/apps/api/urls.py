from django.conf.urls import include, patterns
from django.http import HttpResponseNotFound
from tastypie.api import Api
from logistics_project.apps.api.resources import v0_1
from dimagi.utils.decorators import inline

API_LIST = (
    ((0, 1), (
        v0_1.ProductResources,
        v0_1.WebUserResources,
        v0_1.LocationResources,
        v0_1.SMSUserResources,
        v0_1.StockTransactionResources,
        v0_1.ProductStockResources,
        v0_1.SupplyPointStatusResource,
        v0_1.DeliveryGroupReportResources,
        v0_1.OrganizationSummaryResource,
        v0_1.GroupSummaryResource,
        v0_1.ProductAvailabilityDataResource,
        v0_1.AlertResources,
        v0_1.OrganizationTreeResources
    )),
)

class ILSApi(Api):
    def top_level(self, request, api_name=None, **kwargs):
        return HttpResponseNotFound()

@inline
def api_url_patterns():
    for version, resources in API_LIST:
        api = ILSApi(api_name='v%d.%d' % version)
        for R in resources:
            api.register(R())
        yield (r'^', include(api.urls))

urlpatterns = patterns('',
    *list(api_url_patterns))