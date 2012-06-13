import hashlib

def populate_obj_w_import_data(obj, import_data, mapping=None):
    # Notice the the -1. This is because the data has a blank after attribute at the end of each row
    if not mapping:
        mapping = obj.IMPORT_MAPPING
    for index in range(0, len(mapping)):
        if import_data[index]:
            value = import_data[index]
        else:
            value = None
        setattr(obj, mapping[index], value)
        
def create_checksum(data_list):
    checksum = hashlib.md5()
    for data in data_list:
        if data:
            checksum.update(str(data))
        else:
            checksum.update('')
    return checksum