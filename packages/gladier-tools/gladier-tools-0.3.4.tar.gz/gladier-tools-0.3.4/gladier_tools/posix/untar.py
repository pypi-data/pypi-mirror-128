from gladier import GladierBaseTool, generate_flow_definition


def untar(**data):
    import tarfile
    import pathlib

    untar_input = pathlib.Path(data['untar_input']).expanduser()
    untar_output = None
    if data.get('untar_output', ''):
        untar_output = pathlib.Path(data['untar_output']).expanduser()

    with tarfile.open(untar_input) as file:
        if untar_output:
            untar_output.mkdir(parents=True)
            file.extractall(untar_output)
        else:
            file.extractall()
    return str(untar_output)

@generate_flow_definition(modifiers={
    'untar': {'ExceptionOnActionFailure': True,
              'WaitTime': 300}
})
class UnTar(GladierBaseTool):
    """
    The UnTar tool makes it possible to extract data from Tar archives.

    :param untar_input: Input directory to archive.
    :param untar_output: (optional) output file to save the new archive. Defaults to the original  # noqa
                       input file with an extension '.tgz' removed.
    :param funcx_endpoint_compute: By default, uses the ``compute`` funcx endpoint.  # noqa
    :returns path: The name of the newly created archive.
    """
    
    funcx_functions = [untar]
    required_input = [
            'untar_input',
            'funcx_endpoint_compute',
        ]
