import datetime


# if a package must be delivered before 11 am in the morning add to morning deliveries list
def fill_morning_list(package_time, package_notes):
    if isinstance(package_time, str):
        return False
    if package_time.hour < 11 and package_notes == '':
        return True
    else:
        return False


# if package must be on truck 1 add to truck 1 only list
def fill_truck1_only_list(package_notes):
    if str(package_notes).lower().__contains__('truck 1'):
        return True
    else:
        return False


# if package must be on truck 2 add to truck 2 only list
def fill_truck2_only_list(package_notes):
    if str(package_notes).lower().__contains__('truck 2'):
        return True
    else:
        return False


# if a package has no deadline or notes add to list for deliveries that can happen anytime
def fill_anytime_list(package_time, package_notes):
    if package_time == "EOD" and package_notes == '':
        return True
    else:
        return False


# if a package has not deadline but is delayed add to list for late deliveries
def fill_late_list(package_time, package_notes):
    if (package_time == "EOD" and str(package_notes).lower().__contains__('delayed')) or (
            package_time == "EOD" and str(package_notes).lower().__contains__('wrong address')):
        return True
    else:
        return False


# if a package has correlation to other packages in the notes, extract that correlation store it
def deal_with_aux_packages(package_notes):
    if str(package_notes).lower().__contains__('must be delivered with'):
        # get correlated packages from notes
        correlated_packages = str(package_notes).split(',')
        for s_index, s in enumerate(correlated_packages):
            correlated_packages[s_index] = int(
                ''.join(letter for letter in correlated_packages[s_index] if letter.isdigit()))
        # find the most specific list
        return correlated_packages
