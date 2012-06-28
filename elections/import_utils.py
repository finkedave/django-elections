import hashlib
from datetime import datetime
import locale
def populate_obj_w_import_data(obj, import_data, mapping=None):
    """ Populate an object with import data is is mappied
    by attribute IMPORT_MAPPING """
    if not mapping:
        mapping = obj.IMPORT_MAPPING
    for index in range(0, len(mapping)):
        if import_data[index]:
            value = import_data[index]
        else:
            value = None
        setattr(obj, mapping[index], value)
        
def create_checksum(data_list):
    """ Create a checksum based on a data_list """
    checksum = hashlib.md5()
    for data in data_list:
        if data:
            checksum.update(str(data))
        else:
            checksum.update('')
    return checksum

def normalize_data(data_list, do_normalize_currency=False):
    """ Normalize data. One of the big issues is from the import
    file a empty column is seen as '' instead of None. So turn all
    '' into Nones so we can assume no field id ''. This is important
    to to numbers being inserted into the DB. Django checks for a value
    equal to None before it tries to insert it  """
    normalized_data = []
    for data in data_list:
        if data == "":
            normalized_data.append(None)
        else:
            if do_normalize_currency:
                normalized_data.append(normalize_currency(data))
            else:
                normalized_data.append(data)
    return normalized_data

def normalize_currency(data):
    if data.count('$') == 0:
        return data
    data = data.replace('$', '')
    locale.setlocale( locale.LC_NUMERIC, 'en_US.UTF-8' ) 
    data = str(locale.atof(data))
    return data

def create_date(date_string):
    try:
        date = datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        try:
            date = datetime.strptime(date_string, "%Y-%m").date()
        except:
            try:
                date = datetime.strptime(date_string, "%m-%d-%Y").date()
            except:
                try:
                    date = datetime.strptime(date_string, "%m-%Y").date()
                except:
                    raise ValueError("Date %s doesn't match any known formats" % date_string)
    return date
        