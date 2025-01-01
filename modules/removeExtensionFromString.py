import os

def removeExtensionKeyword(filename):
    name_without_extension = os.path.splitext(filename)[0]
    return name_without_extension
