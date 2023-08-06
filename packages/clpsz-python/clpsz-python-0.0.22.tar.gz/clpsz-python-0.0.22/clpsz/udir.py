import os


# not include files in subdirectories
def get_files_from_dir(dir_path, full_path=True):
    result = []
    for (_dir, dir_names, filenames) in os.walk(dir_path):
        if not os.path.samefile(_dir, dir_path):
            break
        for filename in filenames:
            if full_path:
                result.append(os.path.join(_dir, filename))
            else:
                result.append(filename)
    return result


# not include files in subdirectories
def get_sub_dirs_from_dir(dir_path, full_path=True):
    result = []
    for (_dir, dir_names, filenames) in os.walk(dir_path):
        if not os.path.samefile(_dir, dir_path):
            break
        for dir_name in dir_names:
            if full_path:
                result.append(os.path.join(_dir, dir_name))
            else:
                result.append(dir_name)
    return result


if __name__ == '__main__':
    for e in get_sub_dirs_from_dir('/Users/clpsz/workspace/database-scripts-ng'):
        print(e)
