import os
from gladier_tools.posix.tar import tar


def test_tar_home_directory(mock_tar):
    output_file = tar(tar_input='~/foo')
    assert output_file == os.path.expanduser('~/foo.tgz')


def test_tar(mock_tar):
    mock_open, mock_context_manager = mock_tar
    output_file = tar(tar_input='foo')
    assert mock_open.called
    assert mock_context_manager.add.called
    assert output_file == 'foo.tgz'


def test_tar_trailing_slash(mock_tar):
    """This previously could result in /foo/.tgz"""
    output_file = tar(tar_input='/foo/')
    assert output_file == '/foo.tgz'
