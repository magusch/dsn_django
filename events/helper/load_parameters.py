from django.core.cache import cache
from ..models import Parameter


class ParametersManager:
    CACHE_KEY = 'parameters'
    LOCK_KEY = 'parameters_lock'

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            if not hasattr(cls, '_instance'):
                cls._instance = super().__new__(cls)
                cls._instance.load_parameters_from_cache()
        return cls._instance

    def load_parameters_from_cache(self):
        self._parameters = cache.get(self.CACHE_KEY)
        if not self._parameters:
            self.load_parameters_from_db()

    def load_parameters_from_db(self):
        parameters = Parameter.objects.filter(site='dsn_site').all()
        self._parameters = {param.parameter_name: param.value for param in parameters}
        self.save_parameters_to_cache()

    def save_parameters_to_cache(self):
        cache.set(self.CACHE_KEY, self._parameters, timeout=43200)

    def get_parameter(self, parameter_name):
        self.load_parameters_from_cache()
        return self._parameters.get(parameter_name)

    def update_parameters_from_db(self):
        self.load_parameters_from_db()

    def periodic_update(self):
        self.update_parameters_from_db()
