#!/usr/bin/env python
import os


def main():

    fname = './my_file.txt'

    # check if file exists
    if os.path.isfile(fname):
        print 'removing', fname
        os.remove(fname)

    # open a file
    f = open(fname, 'w')  # Bad style: use 'with' statement

    # write to file
    f.write('monty')

    # close file
    f.close()

    with open(fname, 'a') as f:  # Good style: f.close() always called at the end of block 'wtih'
        f.write('-python')

    # read file content
    with open(fname, 'r') as f:
        content = f.read()  # read all file content

    print 'content of', fname, ':', content

    d = '.'
    if os.path.isdir(d):
        print d, 'is a dir'

    # ├── data
    # │   └── dir1
    # │       ├── 2.txt
    # │       ├── subdir1
    # │       │   └─ 1.txt
    # │       └── subdir2
    # │           └─ 3.txt




if __name__ == '__main__':
    main()
