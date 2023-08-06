# standard
import sys
import platform
from os import system
from os.path import abspath
from os.path import dirname
from os.path import join


def get_platform_bin():
    plt = lambda s: 'vrelease-' + s
    osys = platform.system()

    if osys == 'Linux':
        return plt('linux')

    if osys == 'Darwin':
        return plt('macos')

    if osys == 'Windows':
        return plt('windows.exe')

    raise RuntimeError('unsupported platform ' + osys)


def main():
    try:
        arch = platform.machine()
        if arch not in ('x86_64', 'AMD64'):
            raise RuntimeError('unsupported architecture ' + arch)

        file = get_platform_bin()
        bin_path = abspath(join(dirname(__file__), 'bin', file))

        cli_input = sys.argv[1:]
        cmd = '{} {}'.format(bin_path, ' '.join(cli_input)).strip()
        system(cmd)

    except Exception as err:  # pylint: disable=broad-except
        print(str(err))
        sys.exit(2)


if __name__ == '__main__':
    main()
