__all__ = ['convert']

import os
import base64
from .utils.log_module import Logs

_logger = Logs()


def base64_template(image_base64: str) -> str:
    temp = f'<p><span class="md-image"><img alt="img" src="{image_base64}" referrerpolicy="no-referrer"></span></p>'
    return temp


def get_file_extend(file_path: str) -> str:
    return os.path.splitext(file_path)[1][1:]


def file_to_base64(file_path: str) -> str:
    with open(file_path, 'rb') as f:
        pre_fix = f'data:image/{get_file_extend(file_path)};base64,'
        image_bytes = f.read()
        image_base64 = pre_fix + base64.b64encode(image_bytes).decode('utf8')
        return image_base64


@_logger.decorator('base64 error')
def convert(file_path: str) -> str:
    return base64_template(file_to_base64(file_path))
