class IntCode:
    ADD = 1
    MUL = 2

    def __init__(self, code: list[int]):
        self.og_code = code.copy()
        self.code = code.copy()
        self.pc = 0

    def run_until_end(self) -> 'IntCode':
        pass
        while self.code[self.pc] != 99:
            instr = self.code[self.pc]
            match instr:
                case self.ADD:
                    self.code[self.code[self.pc + 3]] = self.code[self.code[self.pc + 1]] + self.code[self.code[self.pc + 2]]
                    self.pc += 4
                case self.MUL:
                    self.code[self.code[self.pc + 3]] = self.code[self.code[self.pc + 1]] * self.code[self.code[self.pc + 2]]
                    self.pc += 4
                case _:
                    raise NotImplementedError
        return self