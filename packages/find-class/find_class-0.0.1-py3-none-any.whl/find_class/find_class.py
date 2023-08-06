
def find_class(full_name):
    try:
        module_name = '.'.join(full_name.split('.')[:-1])
        class_name = full_name.split('.')[-1]
        module = __import__(module_name, fromlist=[class_name])
        return getattr(module, class_name) 
    except Exception as e:
        return None