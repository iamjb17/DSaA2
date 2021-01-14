import datetime
import sys
import DataInput


# O(n)
# Function that runs the UI of the the application and allows for the user input until application exits
def run_ui(delivery_data):
    input_value = ''
    print('Work Day Summary')
    print('total miles(all trucks):', delivery_data[1], 'end time:', delivery_data[2].time())
    print('packages delivered:', len(delivery_data[0]), 'All packages delivered on time')
    print()
    while input_value != 'exit':
        print('You have 3 options to query the package data:')
        print("1.) Enter package ID number(1-40).")
        print("2.) Enter a time (hh:mm). Returns status of all package status at that specific time.")
        print("3.) Enter 'exit' to end the application.")
        input_value = input()
        if input_value.lower() == 'exit':
            exit_app()
        elif input_value.isnumeric():
            package_lookup(input_value, delivery_data)
            pass
        else:
            try:
                datetime.datetime.strptime(input_value, '%I:%M')
                delivery_time_lookup(input_value, delivery_data)
            except ValueError:
                print('Input Value not recognized! Try again')
        pass


# Exit the application
def exit_app():
    print("Exiting......Complete. Bye")
    sys.exit(0)


# O(1)
# lookup function that returns the package with the specified time
def package_lookup(package_id, data):
    packages = DataInput.Data.packages
    package_id = int(package_id)
    if data[0].get(package_id) is not None:
        package_data = data[0].get(package_id)
        package = packages.find(package_id).getValue()
        d_status = package_data.get_delivery_status()
        d_time = package_data.get_delivery_time().time()
        p_deadline = package.get_deadline()
        if isinstance(p_deadline, str):
            p_deadline = 'EOD'
        else:
            p_deadline = p_deadline.time()
        print('ID:', package.get_id(), 'Address:', package.get_address(), 'Deadline:', p_deadline, 'City:',
              package.get_city(), 'Zip:', package.get_zip(), 'Weight:', package.get_weight(), 'Status:', d_status,
              d_time)
    else:
        print('Package not found! Try again')


# O(n)
# lookup function that returns all package statuses at the specified time
def delivery_time_lookup(input_time, data):
    packages = DataInput.Data.packages
    at_hub = 'At HUB'
    enroute = 'Enroute'
    load_2_time = data[3]
    input_time = datetime.datetime.strptime(input_time, '%H:%M').time()
    for package in packages:
        p_id = package.getValue().get_id()
        package = package.getValue()
        package_data = data[0].get(p_id)
        d_status = package_data.get_delivery_status()
        d_time = package_data.get_delivery_time().time()
        if isinstance(package.get_deadline(), str):
            p_deadline = 'EOD'
        else:
            p_deadline = package.get_deadline().time()

        # x start1 x  -> start2 -> start3
        if input_time < data[7]:
            d_status = at_hub
            d_time = ''
        elif input_time < data[8]:
            if p_id in data[5] and p_id in data[6]:
                d_status = at_hub
                d_time = ''
            else:
                if input_time < d_time:
                    d_status = enroute
                    d_time = ''
        elif input_time < load_2_time:
            if p_id in data[6]:
                d_status = at_hub
                d_time = ''
            elif input_time < d_time:
                d_status = enroute
                d_time = ''
        else:
            if input_time < d_time:
                d_status = enroute
                d_time = ''
        print('ID:', package.get_id(), 'Address:', package.get_address(), 'Deadline:', p_deadline, 'City:',
              package.get_city(), 'Zip:', package.get_zip(), 'Weight:', package.get_weight(),
              'Status:', d_status, d_time)
