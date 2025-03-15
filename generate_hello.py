#!/usr/bin/env python3

import os
import sys

out_dir = sys.argv[1]
cc_file = sys.argv[2]

def write_if_changed(path, contents):
    if not os.path.exists(path):
        with open(path, 'w') as fp:
            fp.write(contents)
        return

    with open(path) as old_fp:
        old_contents = old_fp.read()

    if contents != old_contents:
        with open(path, 'w') as fp:
            fp.write(contents)


write_if_changed(f'{out_dir}/{cc_file}', r'''\
#include <iostream>

#include "bar.h"

int main(int argc, const char **argv) {
  std::cout << "hello " << bar() << "\n";
}
''')
