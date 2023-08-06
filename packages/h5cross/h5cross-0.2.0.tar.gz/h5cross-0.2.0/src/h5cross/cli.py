""" Command line module of h5cross"""

import click


@click.group()
def main_cli():
    """---------------    H5CROSS  --------------------

You are now using the Command line interface of h5cross
a Python3 helper to explore and compare hdf5 files, created at CERFACS (https://cerfacs.fr).


This is a python package currently installed in your python environement.
"""


@click.command()
@click.argument("filename", nargs=1)
def tree(filename):
    """Print the content of an hdf5 file in terminal.
    """
    from h5cross.visit_h5 import get_h5_structure
    from h5cross.utils import print_dict

    print_dict(get_h5_structure(filename))


main_cli.add_command(tree)


@click.command()
@click.argument("filename", nargs=1)
@click.option('--yaml-filename', required=False, default=None, type=str,
              help='default = None , if specified used as YAML output name. \
                            If not specified output name = filename.yml')
@click.option('--yaml-indent', required=False, default=2, type=int,
              help='default = 2, sets the indentation level in ouput YAML file')
def dump(filename, yaml_filename, yaml_indent):
    """Write the content of an hdf5 file into a YAML file.

    """
    from h5cross.visit_h5 import get_h5_structure
    from h5cross.io import write_dict_to_yaml

    mydict = get_h5_structure(filename)
    writename = yaml_filename if yaml_filename is not None else filename.split('.')[0]

    write_dict_to_yaml(mydict, writename, yaml_indent)


main_cli.add_command(dump)


@click.command()
@click.argument("filename", nargs=1)
@click.option('--test', is_flag=True, hidden=True)
def view(filename, test):
    """Show the content of an hdf5 file interactively with nobvisual.
    """
    from h5cross.nobvisual import visual_h5

    visual_h5(filename, start_mainloop=not test)


main_cli.add_command(view)


@click.command()
@click.argument("filename", nargs=1)
@click.option('--pretty', is_flag=True,
              help='Controls if pretty table output is used')
@click.option('--pretty-full-path', is_flag=True,
              help='Controls if full paths in nested dictionary are output in pretty table')
@click.option('--save-as-yaml', is_flag=True,
              help='Default output name is set to input file name')
@click.option('--yaml-filename', required=False, default=None, type=str,
              help='default = None, if specified used as output name of YAML file')
@click.option('--yaml-indent', required=False, default=2, type=int,
              help='default = 2, sets the indentation level in ouput YAML file')
def stats(filename, pretty, pretty_full_path, save_as_yaml, yaml_filename,
          yaml_indent):
    """Compute statistics of arrays from hdf5 file.
    """
    from h5cross.visit_h5 import get_h5_structure
    from h5cross.stats import compute_dict_stats
    from h5cross.io import load_hdf_as_dict
    from h5cross.io import write_dict_to_yaml
    from h5cross.utils import merge_dicts
    from h5cross.utils import print_dict

    data_dict = load_hdf_as_dict(filename)
    stats = compute_dict_stats(data_dict)

    if save_as_yaml or (not pretty):
        h5_struct = get_h5_structure(filename, as_dict=False)
        new_dict = merge_dicts(h5_struct, stats, as_dict=True)

    if pretty:
        from h5cross.prettytable import get_stats_table
        stats_table = get_stats_table(stats, full_path=pretty_full_path)
        print(stats_table)

    else:
        print_dict(new_dict)

    if save_as_yaml:
        writename = yaml_filename if yaml_filename is not None else filename.split('.')[0]
        write_dict_to_yaml(new_dict, writename, yaml_indent)


main_cli.add_command(stats)


@click.command()
@click.argument("file_left", nargs=1)
@click.argument("file_right", nargs=1)
@click.option('--add-stats', is_flag=True,
              help='It computes statistics for each file before comparing')
@click.option('--test', is_flag=True, hidden=True)
def diff(file_left, file_right, add_stats, test):
    """Compare the content of two hdf5 files and view interactively with nobvisual.
    """
    from h5cross.nobvisual import compare_h5

    compare_h5(file_left, file_right, add_stats, start_mainloop=not test)


main_cli.add_command(diff)


@click.command()
@click.argument("file_left", nargs=1)
@click.argument("file_right", nargs=1)
@click.option('--select-vars', required=True, default=None, type=str,
              help='default = None, select variables to plot. Requires a comma separated string with \
            variables to select, e.g. \"temperature,pressure\" ')
@click.option('--save-name', required=False, default=None, type=str,
              help='default = None, string specifying desired output base name for each plot')
@click.option('--use-seaborn', is_flag=True,
              help='Controls the use of seaborn, otherwise matplotlib is used.')
@click.option('--add-xy', is_flag=True,
              help='Superimposes the x=y line on the scatter plot.')
@click.option('--test', is_flag=True, hidden=True)
def scatter(file_left, file_right, select_vars, save_name, use_seaborn, add_xy,
            test):
    """ Scatter plot comparison of two hdf5 files.
        Seaborn is used to generate the plots but can
        be deactivated in which case matplotlib.pyplot is used.

        Note: The matplotlib package is a minimal requirement for this functionality.

    """
    from h5cross.plotting import compare_scatter_h5

    var_list = select_vars.split(",")
    compare_scatter_h5(file_left, file_right, var_list, save_name=save_name,
                       flag_show=not test, flag_seaborn=use_seaborn,
                       flag_xy_line=add_xy)


main_cli.add_command(scatter)


@click.command()
@click.argument("filename", nargs=1)
@click.option('--file-type', required=True, type=click.Choice(['nek5000', 'pvtu', 'vtu', 'vtk']), default=None,
              help='default = None, input format to convert to hdf5')
@click.option('--out-name-h5', required=False, default=None, type=str,
              help='Optional output name for hdf5 file, default = dump.h5')
@click.option('--out-location-h5', required=False, default=None, type=str,
              help='Optional path where to save the hdf5 file, default = current dir')
def convert(filename, file_type, out_name_h5, out_location_h5):
    """ Conversion to hdf5 of certain file formats.
        Currently supported:
            - nek5000: requires "pymech" package
            - vtk: pvtu, vtu   requires "vtk" package
    """
    # TODO: write_h5

    from h5cross.convert import convert
    from h5cross.io import write_h5

    tmp_dict = convert(filename, file_type)

    if out_name_h5 is not None:
        if out_location_h5 is not None:
            write_h5(tmp_dict, save_name_=out_name_h5, save_path_=out_location_h5)
        else:
            write_h5(tmp_dict, save_name_=out_name_h5)
    else:
        if out_location_h5 is not None:
            write_h5(tmp_dict, save_path_=out_location_h5)
        else:
            write_h5(tmp_dict)


main_cli.add_command(convert)
