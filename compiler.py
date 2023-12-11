class Compiler:
    def __init__(self):
        self._command_mapping_ = {
            "->": self.equal,
            "+": self.add,
            "-": self.sub,
            "*": self.mul,
            "/": self.div,
            "%": self.res,
            "==": self.eq,
            "!=": self.ne,
            ">=": self.ge,
            "<=": self.le,
            "!": self.ne,
            "|": self.bw_or,
            "&": self.bw_and,
            "scan": self.scan,
            "print": self.my_print,
            "goto": self.goto,
            "if": self.if_then,
        }

        self._comment_symbol_ = r"\\"
        self._operations_priority_ = ['!', '*', '/', '%', '+', '-', '<=', '>=', '==', '!=', '|', '&']

        self._memory_ = {}
        self._memory_pointer_ = 0
        self._program_counter_ = 0
        self._if_flag_ = 0

        self._compilation_graph_ = []

    def validate_value(self, value: str | int) -> int:
        try:
            return int(value)
        except Exception as error:
            if value in self._memory_:
                return self._memory_.get(value)
            elif value[1:] in self._memory_:
                return self._memory_.get(value[1:])
            else:
                print(error)

                raise Exception("Variable not found")

    def validate_variable(self, value: str) -> str:
        for symbol in value:
            if symbol in self._command_mapping_:
                raise Exception("Bad variable name")

        return value.replace(" ", "")

    def is_expression(self, line: list[str, ...]) -> bool:
        for sign in self._operations_priority_:
            if sign in line:
                return True

        return False

    def format_line(self, line: str) -> str:
        # line = line.replace(" ", "")
        #
        # for symbol in list(self._command_mapping_) + ["then"]:
        #     line = line.replace(symbol, " " + symbol + " ")
        #
        # if "if" in line:
        #     line = line.replace("if", "if ")
        #
        # elif "goto" in line:
        #     line = line.replace("goto", "goto ")

        return line

    def is_mark(self, line: str) -> bool:
        return line in self._memory_ and line[0] == "&"

    def parse_expression(self, line: list[str, ...], command_index: int) -> None:
        if len(line) == 1:
            if line[0] in self._command_mapping_:
                raise Exception("Incorrect operations usega")
            else:
                self._memory_pointer_ += 1

                self._memory_[str(self._memory_pointer_)] = self.validate_value(line[0])

                return

        while len(line) > 1:
            for symbol in self._operations_priority_:
                index = -1

                for part in line:
                    index += 1

                    if symbol == part == "!":
                        self._memory_pointer_ += 1

                        self._compilation_graph_[command_index].append(
                            f"! {self.validate_value(line[index + 1])} ${self._memory_pointer_}")

                        line.pop(index)
                        line[index] = f"${self._memory_pointer_}"

                        continue

                    if symbol == part:
                        self._memory_pointer_ += 1

                        self._compilation_graph_[command_index].append(
                            f"{symbol} {line[index - 1]} {line[index + 1]} ${self._memory_pointer_}")

                        line.pop(index - 1)
                        line.pop(index - 1)
                        line[index - 1] = f"${self._memory_pointer_}"

                        continue

    def parse_equality(self, line: list[str, ...], index: int) -> None:
        if len(line) < 3:
            raise Exception("Incorrect equality using")

        variable = line[0]

        self.parse_expression(line[2:], index)

        self._compilation_graph_[index].append(f"-> {variable} ${self._memory_pointer_}")

    def parse_print(self, line: str, index: int) -> None:
        try:
            self._compilation_graph_[index].append(f"print ${int(line[6:-1])}")
        except ValueError:
            self._compilation_graph_[index].append(f"print {line[6:-1]}")

    def parse_scan(self, line: str, index: int) -> None:
        try:
            self._compilation_graph_[index].append(f"scan ${int(line[5:-1])}")
        except ValueError:
            self._compilation_graph_[index].append(f"scan {line[5:-1]}")

    def parse_if(self, line: list[str, ...], index: int) -> None:
        expression = []
        without_if = line[1:]

        i = 0

        while without_if[i] != "then":
            expression.append(without_if[i])

            i += 1

        assert len(without_if) > 3, "By now impossible"

        self.parse_expression(expression, index)

        self._compilation_graph_[index].append(f"if")

        self.parse_goto(line[-2:], index)

    def parse_goto(self, line: list[str, ...], index: int) -> None:
        if len(line) != 2:
            raise Exception("Incorrect goto usage")

        address = line[-1]

        if self.is_mark("&" + address):
            self.parse_mark("&" + address, index)

            return

        self._compilation_graph_[index].append(f"goto {int(address) - 1}")

    def parse_mark(self, mark: str, index: int) -> None:
        self._compilation_graph_[index].append(f"goto {self._memory_.get(mark)}")

    def compile(self, file_path: str) -> None:
        with open(file_path, "r") as file:
            lines = file.readlines()

            self._compilation_graph_ = [[] for _ in range(len(lines))]

            for index, line in enumerate(lines):
                if line == "\n" or line[:2] == self._comment_symbol_:
                    continue

                line = line.replace("\n", "")
                line = self.format_line(line)

                if ":" in line:
                    mark = "&" + line.split(":")[0]

                    self._memory_[mark] = index

            for index, line in enumerate(lines):
                if line == "\n" or line[:2] == self._comment_symbol_:
                    continue

                line = line.replace("\n", "")
                line = self.format_line(line)

                if ":" in line:
                    mark = "&" + line.split(":")[0]

                    if mark in self._memory_:
                        continue
                    else:
                        raise Exception("Unknown mark name")

                splitted = line.split(" ")

                if "->" in line:
                    self.parse_equality(splitted, index)
                elif "print" in line:
                    self.parse_print(line, index)
                elif "scan" in line:
                    self.parse_scan(line, index)
                elif "if" in line:
                    self.parse_if(splitted, index)
                elif "goto" in line and "if" not in line:
                    self.parse_goto(splitted, index)
                else:
                    print(f"""Seems statement {index + 1}: {line} has no effect""")

    def run(self) -> int:
        while self._program_counter_ < len(self._compilation_graph_):
            layer = self._compilation_graph_[self._program_counter_]

            for command in layer:
                splitted = command.split(" ")
                operation = splitted[0]

                if len(command) > 1:
                    arguments = splitted[1:]
                else:
                    arguments = []

                if self._command_mapping_.get(operation)(*arguments):
                    break

            self._program_counter_ += 1

        return 0

    def equal(self, variable: str, memory: str) -> None:
        self._memory_[variable] = self._memory_[memory[1:]]

    def add(self, first: str, second: str, destination: str) -> int:
        try:
            self._memory_[destination[1:]] = self.validate_value(first) + self.validate_value(second)

            return 0
        except Exception as error:
            print(error)

    def sub(self, first: str, second: str, destination: str) -> int:
        try:
            self._memory_[destination[1:]] = self.validate_value(first) - self.validate_value(second)

            return 0
        except Exception as error:
            print(error)

    def div(self, first: str, second: str, destination: str) -> int:
        try:
            self._memory_[destination[1:]] = self.validate_value(first) // self.validate_value(second)

            return 0
        except Exception as error:
            print(error)

    def mul(self, first: str, second: str, destination: str) -> int:
        try:
            self._memory_[destination[1:]] = self.validate_value(first) * self.validate_value(second)

            return 0
        except Exception as error:
            print(error)

    def res(self, first: str, second: str, destination: str) -> int:
        try:
            self._memory_[destination[1:]] = self.validate_value(first) % self.validate_value(second)

            return 0
        except Exception as error:
            print(error)

    def ne(self, first: str, second: str, destination: str) -> int:
        try:
            self._memory_[destination[1:]] = int(self.validate_value(first) != self.validate_value(second))

            self._if_flag_ = int(self.validate_value(first) != self.validate_value(second))

            return not self._if_flag_
        except Exception as error:
            print(error)

    def eq(self, first: str, second: str, destination: str) -> int:

        try:
            self._memory_[destination[1:]] = int(self.validate_value(first) == self.validate_value(second))

            self._if_flag_ = int(self.validate_value(first) == self.validate_value(second))

            return not self._if_flag_
        except Exception as error:
            print(error)

    def ge(self, first: str, second: str, destination: str) -> int:
        try:
            self._memory_[destination[1:]] = int(self.validate_value(first) >= self.validate_value(second))

            self._if_flag_ = int(self.validate_value(first) >= self.validate_value(second))

            return not self._if_flag_
        except Exception as error:
            print(error)

    def le(self, first: str, second: str, destination: str) -> int:
        try:
            self._memory_[destination[1:]] = int(self.validate_value(first) <= self.validate_value(second))

            self._if_flag_ = int(self.validate_value(first) <= self.validate_value(second))

            return not self._if_flag_
        except Exception as error:
            print(error)

    def bw_or(self, first: str, second: str, destination: str) -> int:
        try:
            self._memory_[destination[1:]] = self.validate_value(first) | self.validate_value(second)

            return 0
        except Exception as error:
            print(error)

    def bw_and(self, first: str, second: str, destination: str) -> int:
        try:
            self._memory_[destination[1:]] = self.validate_value(first) & self.validate_value(second)

            return 0
        except Exception as error:
            print(error)

    def not_op(self, first: str, destination: str) -> int:
        try:
            self._memory_[destination[1:]] = int(not self.validate_value(first))

            return 0
        except Exception as error:
            print(error)

    def scan(self, destination: str) -> None:
        if destination[0] == "$":
            self._memory_[destination[1:]] = self.validate_value(input(">> "))
        else:
            self._memory_[destination] = self.validate_value(input(">> "))

    def my_print(self, first: str) -> None:
        if first[0] == "$":
            print(self._memory_.get(first[1:]))
        else:
            print(self._memory_.get(first))

    def goto(self, first: str) -> None:
        self._program_counter_ = self.validate_value(first)

    def if_then(self) -> int:
        return not self._if_flag_
