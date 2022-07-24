def check_name(name: str):
    """avoid relative path"""
    
    if ".." in name:
        raise ValueError('Invalid name')
