import psutil
import os
import tempfile
from stat import S_ISREG, ST_MTIME, ST_MODE, ST_SIZE


def curate_cache(directory, min_free_percent=5.0, min_free_disk=50):
    """Clear out the directory if needed

    This assumes all the files in the directory can be deleted as freely

    Args:
        directory (str): directory path that holds cached files
        min_free_percent (float): percentage (0.0-100.0) of drive to keep free,
                                  default is 5% if not specified.
        min_free_disk (float): minimum allowed disk space in MB, default
                               value is 50 MB if not specified.
    """

    # Simpleminded implementation -- keep a certain percentage of the
    # disk available.
    # TODO: Would be easy to add more options, like whitelisted files, etc.
    space = psutil.disk_usage(directory)

    # convert from MB to bytes
    min_free_disk *= 1024 * 1024
    # space.percent = space.used/space.total*100.0
    percent_free = 100.0 - space.percent
    if percent_free < min_free_percent and space.free < min_free_disk:
        print('Low diskspace detected, cleaning cache')
        # calculate how many bytes we need to delete
        bytes_needed = (min_free_percent - percent_free) / 100.0 * space.total
        bytes_needed = int(bytes_needed + 1.0)

        # get all entries in the directory w/ stats
        entries = (os.path.join(directory, fn) for fn in os.listdir(directory))
        entries = ((os.stat(path), path) for path in entries)

        # leave only regular files, insert modification date
        entries = ((stat[ST_MTIME], stat[ST_SIZE], path)
                   for stat, path in entries if S_ISREG(stat[ST_MODE]))

        # delete files with oldest modification date until space is freed
        space_freed = 0
        for moddate, fsize, path in sorted(entries):
            try:
                os.remove(path)
                space_freed += fsize
            except Exception:
                pass

            if space_freed > bytes_needed:
                return  # deleted enough!


def get_cache_directory(domain=None):
    """Get a directory for caching data

    This directory can be used to hold temporary caches of data to
    speed up performance.  This directory will likely be part of a
    small RAM disk and may be cleared at any time.  So code that
    uses these cached files must be able to fallback and regenerate
    the file.

    Args:
        domain (str): The cache domain.  Basically just a subdirectory.

    Return:
        str: a path to the directory where you can cache data
    """
    dir = os.path.join(tempfile.gettempdir(), "chatterbpx", "cache")
    return ensure_directory_exists(dir, domain)


def ensure_directory_exists(directory, domain=None):
    """ Create a directory and give access rights to all

    Args:
        domain (str): The IPC domain.  Basically a subdirectory to prevent
            overlapping signal filenames.

    Returns:
        str: a path to the directory
    """
    if domain:
        directory = os.path.join(directory, domain)

    # Expand and normalize the path
    directory = os.path.normpath(directory)
    directory = os.path.expanduser(directory)

    if not os.path.isdir(directory):
        try:
            save = os.umask(0)
            os.makedirs(directory, 0o777)  # give everyone rights to r/w here
        except OSError:
            print("Failed to create: " + directory)
            pass
        finally:
            os.umask(save)

    return directory
