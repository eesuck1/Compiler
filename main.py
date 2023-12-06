from compiler import Compiler


def main():
    compiler = Compiler()

    compiler.compile("test.e")
    compiler.run()


if __name__ == '__main__':
    main()
