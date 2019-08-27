import uuid

class UUID(object):

    @staticmethod
    def get():
        uid = str(uuid.uuid4())
        return ''.join(uid.split('-'))[:8]
