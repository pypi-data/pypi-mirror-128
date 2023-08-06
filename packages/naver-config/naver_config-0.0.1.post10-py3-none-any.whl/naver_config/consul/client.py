import consul
import os


class ConsulClient():
    def __init__(self):
        self.c = consul.Consul(host=os.getenv(
            "CONSUL_HOST"), port=os.getenv("CONSUL_PORT"))
        pass

    def getValue(self, key, index=1):
        try:
            self.index, self.data = self.c.kv.get(key, index=index)
            print(self.data)
            return self.data
        except Exception as e:
            return None

    def setValue(self, key, value):
        try:
            self.c.kv.put(key, value)
            return True
        except Exception as e:
            return None

    def deleteValue(self, key):
        try:
            if self.c.kv.get(key) is not None:
                self.c.kv.delete(key)
                return True
            else:
                return None
        except Exception as e:
            return None

    def createNode(self, node):
        try:
            self.c.catalog.register(node)
            return True
        except Exception as e:
            return None

    def deleteNode(self, node):
        try:
            self.c.catalog.deregister(node)
            return True
        except Exception as e:
            return None

    def registerService(self, service_name):
        try:
            self.c.agent.service.register(service_name)
            return True
        except Exception as e:
            return None
    
    def deregisterService(self, service_name):
        try:
            self.c.agent.service.deregister(service_name)
            return True
        except Exception as e:
            return None 
