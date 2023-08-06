import logging
import os

from ..filetypes.utils import read_file_to_hex_data_by_path, load_signature_by_hex_data, \
    read_file_to_hex_data_by_file_binary

logger = logging.getLogger()


class File(object):

    def __init__(self):
        pass

    @staticmethod
    def validate_input_filepath(filepath):
        if not os.path.isfile(filepath):
            message = "[ERROR] :: filepath %s not exist." % filepath
            logger.error(message)
            raise Exception(message)
        return

    @staticmethod
    def validate_input_extension(extensions):
        if not extensions:
            logger.error("extensions must be exists")
            raise Exception("[ERROR]")
        return

    @staticmethod
    def get_extension_by_filepath(filepath):
        # Validate filepath
        File.validate_input_filepath(filepath)
        hex_data_file = read_file_to_hex_data_by_path(filepath)

        lst_extension = load_signature_by_hex_data(hex_data_file)

        return lst_extension

    @staticmethod
    def get_extension_by_file_binary(file_binary):
        # Validate filepath
        hex_data_file = read_file_to_hex_data_by_file_binary(file_binary)

        lst_extension = load_signature_by_hex_data(hex_data_file)

        return lst_extension

    @staticmethod
    def check_filetype_by_file_extensions(filepath=None, file_binary=None, extensions=None):
        File.validate_input_extension(extensions)
        if filepath:
            lst_extension = File.get_extension_by_filepath(filepath)
        else:
            lst_extension = File.get_extension_by_file_binary(file_binary)
        result_merge_extension = list(set(lst_extension) & set(extensions))
        result = {
            "status": len(result_merge_extension) > 0,
            "extension_of_file": lst_extension
        }
        return result
