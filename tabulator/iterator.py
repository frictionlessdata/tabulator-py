class Iterator(object):
    """Iterator representation.
    """

    # Public

    def __init__(self, bytes, items, processors):
        self.__bytes = bytes
        self.__items = items
        self.__processors = processors
        self.__input_index = 0
        self.__output_index = 0
        self.__keys = None
        self.__values = None
        self.__headers = None
        self.__is_stop = False
        self.__is_skip = False
        self.__exception = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.__is_stop:
            raise StopIteration()
        self.__input_index += 1
        self.__output_index += 1
        self.__keys = None
        self.__values = None
        self.__is_stop = False
        self.__is_skip = False
        try:
            self.__keys, self.__values = next(self.__items)
        except StopIteration:
            raise
        except Exception as exception:
            self.__exception = exception
        if self.__keys is not None:
            self.__headers = self.__keys
        for processor in self.__processors:
            processor.process(self)
            if self.__is_skip:
                break
        if self.__is_skip:
            self.__output_index -= 1
            return self.__next__()
        return self

    def __repr__(self):
        template = 'Iterator <{self.index}, {self.headers}, {self.values}>'
        return template.format(self=self)

    def reset(self):
        try:
            self.__bytes.seek(0)
            self.__input_index = 0
        except Exception:
            message = (
                'Parser\'s returned not seekable byte stream. '
                'For this kind of stream reset is not supported.')
            raise RuntimeError(message)

    def skip(self):
        self.__is_skip = True

    def stop(self):
        self.__is_stop = True

    @property
    def input_index(self):
        return self.__input_index

    @property
    def output_index(self):
        return self.__output_index

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, headers):
        self.__headers = headers

    @property
    def values(self):
        return self.__values

    @values.setter
    def values(self, values):
        self.__values = values

    @property
    def exception(self):
        return self.__exception

    # Python2 support
    next = __next__
