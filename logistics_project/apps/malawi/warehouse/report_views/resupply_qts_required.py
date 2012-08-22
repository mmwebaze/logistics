from logistics.models import StockRequest, Product, SupplyPoint

from logistics_project.apps.malawi.warehouse import warehouse_view
from logistics_project.apps.malawi.util import get_default_supply_point, fmt_pct,\
    facility_supply_points_below


class View(warehouse_view.DistrictOnlyView):

    def custom_context(self, request):
        
        table = {
            "id": "quantity-required-for-resupply",
            "is_datatable" : True,
            "header": ["Facility Name"],
            "data": [],
        }

        emergency = True
        selected_type = "yes"
        if request.GET.get("emergency"):
            selected_type = str(request.GET.get("emergency"))
            emergency = selected_type == "yes"

        sp = SupplyPoint.objects.get(location=request.location)\
            if request.location else get_default_supply_point(request.user)
        
        facilities = facility_supply_points_below(sp.location)
        
        for product in Product.objects.all().order_by('sms_code'):
            table["header"].append(product.name)

        for fac in facilities:
            temp = [fac.name]
            for product in Product.objects.all():
                temp.append(sum([r.amount_requested\
                    for r in StockRequest.pending_requests().filter(supply_point=fac, product=product,\
                        is_emergency=emergency)]))
            table["data"].append(temp)

        table["height"] = min(480, facilities.count()*60)

        return {
                "table": table,
                "selected_type": selected_type
        }