def check_name(name: str):
    """avoid relative path"""
    
    check_list = ['..', '/', '\\', ':']
    if any(elem in name for elem in check_list):
        raise ValueError('Invalid Name')
    
def check_key(keys: list, input_dict: dict):
    """avoid invalid keys"""
    
    if any(key not in keys for key in input_dict):
        raise ValueError('Invalid Key')
