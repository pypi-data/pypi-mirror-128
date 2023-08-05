import binascii
import json

from ..filetypes.common import FILEPATH_SIGNATURE, ParamFileSignature


def read_file_to_hex_data_by_path(filepath):
    # Open in binary mode (so you don't read two byte line endings on Windows as one byte)
    # and use with statement (always do this to avoid leaked file descriptors, unflushed files)
    with open(filepath, 'rb') as f:
        # Slurp the whole file and efficiently convert it to hex all at once
        hex_data = binascii.hexlify(f.read())
    return hex_data


def read_file_to_hex_data_by_file_binary(file_binary):
    hex_data = binascii.hexlify(file_binary.stream.read())
    return hex_data


def load_signature_by_hex_data(hex_data_file):
    results = []
    with open(FILEPATH_SIGNATURE, "r") as f:
        data_signature = f.read()
        data_signature = json.loads(data_signature)
        for extension, signature in data_signature.items():
            lst_signs = signature.get(ParamFileSignature.SIGNS)
            for sign_data in lst_signs:
                signs = sign_data.split(",")
                offset, hex_code = int(signs[0]), signs[1]
                len_hex_code = len(hex_code)
                hex_data_slice = hex_data_file[offset: len_hex_code].decode('utf-8')
                if hex_code.lower() == hex_data_slice.lower() and extension not in results:
                    results.append(extension)
    return results
