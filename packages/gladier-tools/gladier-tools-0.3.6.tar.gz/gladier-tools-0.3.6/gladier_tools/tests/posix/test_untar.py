import os
import pytest
from gladier_tools.posix.untar import untar


def test_untar_no_file():
    with pytest.raises(FileNotFoundError):
        untar(**{'untar_input': 'foo.tar.gz'})


def test_untar_mkdir(mock_tar):
    mock_tf, mock_context_manager = mock_tar
    untar(**{'untar_input': 'foo.tar.gz'})
    # assert mock_mkdir.called
    assert mock_tf.called
    assert mock_context_manager.extractall.called


def test_untar_input_home(mock_tar):
    output_file = untar(untar_input='~/foo.tgz')
    assert output_file == os.path.expanduser('~/foo')


def test_untar_output_home(mock_tar):
    output_file = untar(untar_input='~/foo.tgz', untar_output='~/tmp/bar')
    assert output_file == os.path.expanduser('~/tmp/bar')
