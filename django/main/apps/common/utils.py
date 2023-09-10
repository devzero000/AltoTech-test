def clean_instance_data(instance):
    data = instance.__dict__.copy()
    data.pop('_state', None)
    return data
