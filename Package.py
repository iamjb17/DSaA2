import datetime
import time


class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, mass, notes, distances,
                 delivery_status='At the HUB'):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.mass = mass
        self.notes = notes
        self.distances = distances
        self.delivery_status = delivery_status

    def get_id(self):
        return int(self.package_id)

    def get_address(self):
        return self.address

    def get_deadline(self):
        if self.deadline == 'EOD':
            return self.deadline
        elif isinstance(self.deadline, datetime.datetime):
            return self.deadline
        else:
            p_time = str(self.deadline)
            # print('in package', self.deadline)
            self.deadline = datetime.datetime.strptime(p_time, '%H:%M %p')
            # self.deadline = time.strptime(original_time, '%H:%M %p')
            # print(time.strftime('%I:%M %p', self.deadline))
            return self.deadline.time()

    def get_notes(self):
        return self.notes

    def get_distances(self):
        return self.distances

    def get_delivery_status(self):
        return self.delivery_status

    def set_delivery_status(self, status: str):
        self.delivery_status = self.delivery_status
