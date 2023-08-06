from os import environ

class Config(object):
    storage = {}
    
    def __init__(self):
        for key, replacement in [('ENV', 'Development'), 
                                 ('NAME', 'None'),
                                 ('TYPE', 'None'),
                                 ('DB_URI', 'None'),
                                 ('Elastic_URL', 'localhost'),
                                 ('ELASTIC_PORT', '9200'),]:
            self.storage[key] = environ.get(key) or replacement  

    def get(self, target, replacement=None):
        if target in self.storage:
            return self.storage[target]
        res = environ.get(target)
        if res is None:
            print(f'Could not find {target}')
            return replacement
        self.storage[target] = res
        return res
