from jsonrpcserver import methods
from jsonrpcserver.exceptions import InvalidParams

@methods.add
def hello(**kwargs):
    if 'name' not in kwargs:
        raise InvalidParams('name is required')
    else:
        return dict(message="Hello, %s!" % kwargs['name'])

if __name__ == '__main__':
    methods.serve_forever()
