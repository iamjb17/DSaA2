class Truck:
    def __init__(self):
        self.capacity = 16
        self.storage = [None] * self.capacity

    def add_package(self, package):
        self.storage.append(package)

    def remove_package(self, package):
        self.storage.remove(package)

