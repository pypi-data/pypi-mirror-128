import os
from typing import Iterable, Optional, Union
from darfix.core.dataset import Dataset


def load_process_data(
    filenames: Union[str, Iterable[str]],
    root_dir: Optional[str] = None,
    in_memory: bool = True,
    dark_filename: Optional[str] = None,
    copy_files: bool = True,
    isH5: bool = False,
):
    """When `filenames` is a string, it will be treated as a file pattern."""
    indices = li_indices = None
    root_dir_specified = bool(root_dir)

    if isinstance(filenames, str):
        if not root_dir_specified:
            root_dir = os.path.dirname(filenames)
        dataset = Dataset(
            _dir=root_dir,
            first_filename=filenames,
            in_memory=in_memory,
            copy_files=copy_files,
            isH5=isH5,
        )
    else:
        filenames = list(filenames)
        if not root_dir_specified:
            root_dir = os.path.dirname(filenames[0])
        dataset = Dataset(
            _dir=root_dir,
            filenames=filenames,
            in_memory=in_memory,
            copy_files=copy_files,
            isH5=isH5,
        )

    if dark_filename:
        if root_dir_specified:
            dark_root_dir = os.path.join(root_dir, "dark")
        else:
            dark_root_dir = os.path.dirname(dark_filename)
        bg_dataset = Dataset(
            _dir=dark_root_dir, first_filename=dark_filename,
            copy_files=copy_files, isH5=isH5,
        )
    else:
        bg_dataset = None

    return dataset, indices, li_indices, bg_dataset
