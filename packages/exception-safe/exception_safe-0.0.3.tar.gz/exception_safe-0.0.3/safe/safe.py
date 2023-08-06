def safe(cb, default=None):
    try:
        return cb()
    except Exception as e:
        return default