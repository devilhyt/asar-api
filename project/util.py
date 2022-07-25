def check_name(name: str):
    """avoid relative path"""
    
    check_list = ["..", "/", "\\"]
    if any(elem in name for elem in check_list):
        raise ValueError('Invalid name')
