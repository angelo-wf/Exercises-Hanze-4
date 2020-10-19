
import sys

def get_path(name):
    path = sys.argv[0][::-1]
    index = path.find("/")
    if index == -1:
        return name
    else:
        return (name[::-1] + path[index:])[::-1]
