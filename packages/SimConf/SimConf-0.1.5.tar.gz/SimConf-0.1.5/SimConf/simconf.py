import json
from propertys import *


class SimConf:
    """filename is used to set the name and path of saving attributes,
    example: filename= "config" or filename= "folder/config",
    standard: "config" """
    filename = "config"

    """default_atr is used to define standard values and reset to these
    values if necessary, it can only be a list or a dict and
    contain any attributes inside it,
    example: {atr: "atr", ...} or [atr, ...],
    standard: {} """
    default_atr = {}

    """ensure_ascii takes a boolean value, a standard json attribute"""
    ensure_ascii = True

    """load_conf accepts boolean values, if true, it loads values from
    a file, if there is no file, it uses default_atr, if false, it
    uses default_atr"""
    load_conf = True

    def __init__(self,
                 filename="config", default_atr={},
                 ensure_ascii=True, load_conf=True
                 ):

        self.filename = StrProperty(filename)
        self.default_atr = CustomProperty(default_atr, (dict, list))
        self.ensure_ascii = BoolProperty(ensure_ascii)
        self.load_conf = BoolProperty(load_conf)

        if self.load_conf:
            self.data = self.load()
        else:
            self.data = self.default_atr

    def __str__(self):
        return self.__repr__()

    def __del__(self):
        try:
            self.save()
        except:
            print(f"{self.filename} DONT SAVE")

    def __iter__(self):
        return self.data.__iter__()

    def __setattr__(self, obj, val):
        super().__setattr__(obj, val)
        if obj == "filename" or\
            obj == "default_atr" or\
            obj == "ensure_ascii" or\
            obj == "load_conf":
            return
        self.save()

    def __getitem__(self, key):
        # print(f"Get_item {key} {args}")
        return self.data[key]

    def __setitem__(self, key, val):
        # print(f"{key}\t{val}")
        self.data[key] = val
        self.save()

    def __len__(self):
        return len(self.data)

    def get(self, key):

        if isinstance(self.data, dict):
            return self.data.get(key)
        else:
            try:
                return self.data[key]
            except IndexError:
                return None
            except TypeError:
                raise TypeError("For dict use only index")

    def keys(self):
        if isinstance(self.data, dict):
            return self.data.keys()
        else:
            return [value[0] for value in enumerate(self.data)]

    def values(self):
        if isinstance(self.data, dict):
            return self.data.values()
        else:
            return self.data

    def items(self):
        if isinstance(self.data, dict):
            return self.data.items()
        else:
            return enumerate(self.data)

    def append(self, key, add=None):
        if add == None:
            if isinstance(self.data, list):
                self.data.append(key)
                self.save()
            else:
                raise AttributeError()
        else:
            if isinstance(self.data, dict):
                self.data[key] = add
            else:
                raise AttributeError()

    def load(self):
        try:
            with open(f"{self.filename}.json", "r", encoding="UTF-8") as file:
                return json.load(file)
        except:
            return self.default_atr

    def save(self):
        with open(f"{self.filename}.json", "w", encoding="UTF-8") as file:
            json.dump(self.data, file, ensure_ascii=self.ensure_ascii, indent=4)

    def set_default(self):
        self.data = self.default_atr

    def get_default(self):
        return self.default_atr

    def print_all(self):
        for key, value in self.items():
            print(key, value, sep=" <===> ")
