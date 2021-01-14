# Authored By: Jessie Burton #001356971
import RunRoute
import UI

# Created using PyCharm Community Edition 2020.1.3 x64 on a Lenovo Laptop Running Windows 10 on AMD hardware

# only run this code if I am running as the main entry point of the application
if __name__ == '__main__':
    # * Driver Main Class-- The dominate time complexity is O(n^3), worst case *
    class Main:
        # The primary use of dict data structure was used because 0(1) search feature and ability to self adjust its size to fit the data
        # Main Algorithm used is the Greedy Algorithm, self adjusting
        # O(n^2) + O(n^3)
        delivery_data = RunRoute.run_route()
        # O(n)
        UI.run_ui(delivery_data)
