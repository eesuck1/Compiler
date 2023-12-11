import sys

from compiler import Compiler


def main():
    compiler = Compiler()

    if len(sys.argv) == 1:
        compiler.compile("test.e")
    elif len(sys.argv) == 2:
        compiler.compile(sys.argv[1])
    else:
        raise Exception("Incorrect Compiler Usage")

    compiler.run()


if __name__ == '__main__':
    main()
