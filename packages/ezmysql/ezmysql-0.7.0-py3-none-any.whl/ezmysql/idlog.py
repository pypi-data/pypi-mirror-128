# coding:utf-8


class IDLog:
    '''save & read int ID to/from a file
    '''
    def __init__(self, filename):
        self._fn = filename

    def save_id(self, _id):
        f = open(self._fn, 'w')
        f.write(str(_id))
        f.flush()
        f.close()

    def get_id(self,):
        _id = 0
        try:
            s = open(self._fn).read(32).strip()
            _id = int(s)
        except:
            pass
        return _id
