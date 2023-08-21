import os

def makeDirs(structure, parent_path):
    if isinstance(structure, dict):
        for key, value in structure.items():
            folder_path = os.path.join(parent_path, key)
            os.makedirs(folder_path, exist_ok=True)
            makeDirs(value, folder_path)
    elif isinstance(structure, list):
        for item in structure:
            makeDirs(item, parent_path)
    else:
        pass

def setupDirs():
    folder_structure = {
        "src": {
            "providers": {
                "productDetails": {},
                "products": {}
            },
            "history": {
                "product": {}
            }
        }
    }
    makeDirs(folder_structure, '')

setupDirs()