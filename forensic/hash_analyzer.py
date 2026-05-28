import hashlib
import os

def generate_sha256(file_path):

    if not os.path.exists(file_path):
        return "FILE_NOT_FOUND"
    
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as f:
            
            while chunck := f.read(4096):
                sha256.update(chunck)
        
        return sha256.hexdigest()
    except:
        return "HASH_ERROR"