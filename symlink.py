from os import listdir, unlink, symlink
from os.path import join, islink, expanduser

SYNCPATH = expanduser('~/m@type.hk/system/')
HOMEDIR = expanduser('~')

def create_symlinks(srcdir, dstdir, prefix='', excludes=None):
    for item in listdir(srcdir + prefix):
        if not excludes or item not in excludes:
            src = join(srcdir, prefix, item)
            dst = join(dstdir, prefix, item)
            if islink(dst):
                unlink(dst)
            try:
                symlink(src,dst)
            except FileExistsError:
                print('>> remove existing', dst, 'before symlinking')


if __name__ == '__main__':
    create_symlinks(SYNCPATH, HOMEDIR, excludes=['dotfiles'])
    create_symlinks(SYNCPATH + 'dotfiles/', HOMEDIR, excludes=['beetsconfig','.config', '.local', 'R'])
    create_symlinks(SYNCPATH + 'dotfiles/', HOMEDIR, prefix='.config')
    create_symlinks(SYNCPATH + 'dotfiles/', HOMEDIR, prefix='.local/share')
