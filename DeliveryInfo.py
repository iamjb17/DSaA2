# O(n)
# Uniformly collect and store delivery meta data for reference and review
class DeliveryInfo:
    def __init__(self, package_id, delivery_status, delivery_time, loaded_on_truck_time, delivered=False):
        self.package_id = package_id
        self.delivery_status = delivery_status
        self.delivery_time = delivery_time
        self.loaded_on_truck_time = loaded_on_truck_time
        self.delivered = delivered

    def set_delivery_time(self, time):
        self.delivery_time = time

    def set_delivery_status(self, status):
        self.delivery_status = status

    def get_delivery_time(self):
        return self.delivery_time

    def get_delivery_status(self):
        return self.delivery_status

    def get_loaded_on_truck_time(self):
        return self.loaded_on_truck_time

# O(n)
# merge multiple delivery objects into one dict
def merge(d1, d2, d3):
    first_result = {**d1, **d2}
    final_result = {**first_result, **d3}
    return final_result
