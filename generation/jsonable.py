import json
class Jsonable:
    """
    This parent class is used to define methods for custom objects that are used when writing and reading to and from json
    """
    def to_json(self, path, key, value):
        """Writes class attributes to a json file

        Args:
            path (string): path to write file to
            key (string): key of dictionary to write to file
            value (string): value of dictionary to write to file 
        """
        with open(path, 'r+') as f:
            data = json.load(f)
            data[key] = value
            f.seek(0) 
            json.dump(data, f)
    
    @staticmethod
    def from_json(path):
        """Reads from json file and returns dictionary

        Args:
            path (string): path of file to read from

        Returns:
            Dictionary loaded from json file
        """
        with open(path, 'r') as f:
            data = f.read().replace('"', '\"')
            note = json.loads(data)
        return note

    @staticmethod
    def setup(path):
        """Sets up an empty dictionary at path

        Args:
            path (string): path to write to
        """
        with open(path, 'w') as f:
            json.dump({}, f)