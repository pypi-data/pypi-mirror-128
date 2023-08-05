import pathlib
from gladier_tools.posix.encrypt import encrypt
from unittest.mock import patch, mock_open

MOCK_DATA = bytes('This is a secret file, it shall be encrypted!', 'utf-8')


def test_encrypt():
    with patch('builtins.open', mock_open(read_data=MOCK_DATA)) as mock_file:
        encrypt(**{'encrypt_input': 'foo', 'encrypt_key': 'my_secret'})
    mock_file.assert_called_with(pathlib.Path('foo.aes'), 'wb+')


def test_encrypt_custom_outfile():
    with patch('builtins.open', mock_open(read_data=MOCK_DATA)) as mock_file:
        encrypt(**{'encrypt_input': 'foo', 'encrypt_key': 'my_secret',
                   'encrypt_output': 'bar.aes'})
    mock_file.assert_called_with(pathlib.Path('bar.aes'), 'wb+')