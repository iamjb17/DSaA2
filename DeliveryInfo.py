class DeliveryInfo:
    def __init__(self, package_id, delivery_status, delivery_time, delivered=False):
        self.package_id = package_id
        self.delivery_status = delivery_status
        self.delivery_time = delivery_time
        self.delivered = delivered

    def set_del_time(self, time):
        self.delivery_time = time

    def set_del_status(self, status):
        self.delivery_status = status

def merge(d1,d2, d3):
    first_result = {**d1, **d2}
    final_result = {**first_result, **d3}
    return final_result
