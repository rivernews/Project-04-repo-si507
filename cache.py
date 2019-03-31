class CacheManager:

    def __init__(self, db):
        self.db = db
    
    def get_or_cache(self, key, value_func, value_func_kwargs={}):
        """
            call this function first to get the value
            this function will guarantee you get a value at the end
            it will handle the cache and optimize for you
        """
        cache_object = None

        if self.is_cache_exist():
            cache_object = self.load_cache_content()
        else:
            cache_object = value_func(**value_func_kwargs)
            self.store_cache_content(cache_object)

        return cache_object
    
    def is_cache_exist(self):
        # TODO
        return False
    
    def load_cache_content(self):
        cache_content = None

        # TODO

        return cache_content # should load file ito python variable
    
    def store_cache_content(self, content):
        # TODO

        return