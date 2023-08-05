import os
import sys
import glob
from ewoksorange.bindings.owsconvert import ows_to_ewoks
from darfix.core.process import graph_data_selection


def is_image_file(filename):
    if not os.path.isfile(filename):
        return False
    return all(not filename.endswith(ext) for ext in [".py", ".ows"])


def main(argv=None):
    import argparse

    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        description="Execute a darfix workflow", prog="darfix"
    )
    parser.add_argument("-wf", "--workflow", help="Filename of the workflow", type=str)
    parser.add_argument(
        "-fd",
        "--file_directory",
        help="Directory containing images",
        type=str,
        default=None,
    )
    parser.add_argument(
        "-ff",
        "--first_filename",
        help="Filename to the first file of the stack",
        type=str,
        default=None,
    )
    parser.add_argument(
        "-td",
        "--treated_data",
        help="Directory to save treated data",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--in-disk",
        help="Do not load data into memory",
        dest="in_disk",
        action="store_true",
        default=None,
    )

    options = parser.parse_args(argv[1:])
    if not options.workflow:
        parser.error("Please enter the workflow filename")
    if not (options.file_directory or options.first_filename):
        parser.error("Please enter the file directory or first filename")

    root_dir = options.file_directory
    if options.first_filename:
        filenames = options.first_filename
    else:
        filenames = sorted(
            [x for x in glob.glob(os.path.join(root_dir, "*")) if is_image_file(x)]
        )
    if options.treated_data:
        root_dir = options.treated_data
    in_memory = not options.in_disk

    graph = ows_to_ewoks(options.workflow)
    graph_data_selection(
        graph=graph, filenames=filenames, root_dir=root_dir, in_memory=in_memory
    )
    results = graph.execute()
    for node_id, task in results.items():
        assert task.succeeded, node_id
        print(task.output_values)


if __name__ == "__main__":
    sys.exit(main())
