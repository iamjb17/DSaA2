import datetime


# container object that define what a package looks like and how it acts
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

    # returns a string representation of the object
    def __repr__(self):
        p_id = self.get_id()
        p_address = self.get_address()
        p_deadline = self.get_deadline().time()
        p_city = self.get_city()
        p_zip = self.get_zip()
        p_weight = self.get_weight()
        # p_status_and_time = self.get_delivery_status()
        elem = (p_id, p_address, p_deadline, p_city, p_zip, p_weight)

        return elem.__str__()

    # return package id
    def get_id(self):
        return int(self.package_id)

    # return package address
    def get_address(self):
        return self.address

    # O(1)
    # return package deadline
    def get_deadline(self):
        if self.deadline == 'EOD':
            return self.deadline
        elif isinstance(self.deadline, datetime.datetime):
            return self.deadline
        else:
            p_time = str(self.deadline)
            self.deadline = datetime.datetime.strptime(p_time, '%H:%M %p')
            # self.deadline = time.strptime(original_time, '%H:%M %p')
            # print(time.strftime('%I:%M %p', self.deadline))
            return self.deadline.time()

    # return package notes
    def get_notes(self):
        return self.notes

    # return package distance list based on its location
    def get_distances(self):
        return self.distances

    # return delivery status of the package
    def get_delivery_status(self):
        return self.delivery_status

    # set delivery status of the package
    def set_delivery_status(self, status: str):
        self.delivery_status = status

    # set delivery address of the package
    def set_delivery_address(self, address: str):
        self.address = address

    # set delivery city of the package
    def set_delivery_city(self, city: str):
        self.city = city

    # set delivery state of the package
    def set_delivery_state(self, state: str):
        self.state = state

    # set delivery distances of the package
    def set_delivery_distances(self, distances: str):
        self.distances = distances

    # set delivery zip of the package
    def set_delivery_zip(self, zip_code: str):
        self.zip_code = zip_code

    def get_city(self):
        return self.city

    def get_zip(self):
        return self.zip_code

    def get_weight(self):
        return self.mass
