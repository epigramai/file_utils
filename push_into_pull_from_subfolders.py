import argparse
import os
from functools import reduce
from operator import itemgetter

from file_utils.folder import Folder
from file_utils.py_wrapper import aggregate, lstrip, separate


def get_subfolder_branches(folder, prefix_branches):
    look_deeper, this_is_it = separate(set(prefix_branches), lambda x: x and x[0] in folder.subfolders)

    subfolders = aggregate(look_deeper, set, itemgetter(0), itemgetter(slice(1, None)))

    branch_dct = {}
    for subfolder_name, branches in subfolders.items():
        branch_dct.update(
            {(subfolder_name,) + prefix_branch: [subfolder_name] + subfolder_branch for prefix_branch, subfolder_branch
             in get_subfolder_branches(folder.subfolders[subfolder_name], branches).items()})
    branch_dct.update({k: [] for k in this_is_it})

    return branch_dct


def push_files_into_subfolders(folder, without_prefixes, create_subfolders):
    # TODO: handle edge case filename_with_final_underscore_.ext
    prefix_branches = aggregate(folder.filenames, set, lambda x: tuple(os.path.splitext(x)[0].split('_')[:-1]))

    if not create_subfolders:
        subfolder_branches = get_subfolder_branches(folder, prefix_branches.keys())

    for prefix_branch, filenames in prefix_branches.items():
        if create_subfolders:
            new_branch = prefix_branch
            os.makedirs(os.path.join(folder.path, *new_branch), exist_ok=True)
        else:
            new_branch = subfolder_branches[prefix_branch]
        if not new_branch:
            continue
        subfolder_path = os.path.join(folder.path, *new_branch)
        for filename in filenames:
            if without_prefixes:
                new_filename = lstrip(filename, '_'.join(new_branch + ['']))
            else:
                new_filename = filename
            new_filepath = os.path.join(subfolder_path, new_filename)
            if os.path.exists(new_filepath):
                'WARNING: {} already exists, skipping'.format(new_filepath)
                continue
            os.rename(os.path.join(folder.path, filename), new_filepath)


def pull_files_from_subfolders(folder, without_prefixes, base_path=None, subfolder_branch=None):
    base_path = base_path or folder.path
    subfolder_branch = subfolder_branch or []
    for subfolder_name, subfolder in folder.subfolders.items():
        pull_files_from_subfolders(subfolder, without_prefixes, base_path, subfolder_branch + [subfolder_name])

    for filename in folder.filenames:
        if without_prefixes:
            new_filename = filename
        else:
            new_filename = reduce(lstrip, [x + '_' for x in subfolder_branch], filename)
            new_filename = '_'.join(subfolder_branch + [new_filename])
        os.rename(os.path.join(folder.path, filename), os.path.join(base_path, new_filename))


def process(folder_path, push, pull, without_prefixes, create_subfolders):
    if push and pull:
        print('ERROR: cannot both push and pull files at the same time')
    
    folder = Folder.with_subfolders(folder_path)
    
    if pull:
        pull_files_from_subfolders(folder, without_prefixes)
        
    if push:
        push_files_into_subfolders(folder, without_prefixes, create_subfolders)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Apply name record')
    parser.add_argument('folder_path', help='The location of the image files')
    parser.add_argument('--push', dest='push', action='store_true', help='Push files to subfolders based on prefixes')
    parser.add_argument('--pull', dest='pull', action='store_true', help='Pull files from subfolders, add prefixes')
    parser.add_argument('--without_prefixes', dest='without_prefixes', action='store_true', help='Strip or do not add prefixes')
    parser.add_argument('--create_subfolders', dest='create_subfolders', action='store_true', help='Create subfolders that do not already exist')
    args = parser.parse_args()
    process(args.folder_path, args.push, args.pull, args.without_prefixes, args.create_subfolders)