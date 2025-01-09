from collections import deque
from enum import Enum
from typing import Iterable


class State(Enum):
    READY = 0
    WAIT_INPUT = 1
    WAIT_OUTPUT = 2

class OP(Enum):
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    NZJMP = 5
    ZJMP = 6
    LT = 7
    EQ = 8

class MODE(Enum):
    INDIRECT = 0
    IMMEDIATE = 1

class IntCode:
    def __init__(self, code: list[int]):
        self.og_code = code.copy()
        self.code = code.copy()
        self.pc = 0
        self.state = State.READY
        self.inp = deque()
        self.output = deque()

    def add_input(self, inp: int):
        self.inp.append(inp)
        if self.state == State.WAIT_INPUT:
            self.state = State.READY

    def add_inputs(self, inputs: Iterable[int]):
        self.inp.extend(inputs)
        if self.state == State.WAIT_INPUT:
            self.state = State.READY


    def get_param(self, pos: int, mode: MODE) -> int:
        match mode:
            case MODE.INDIRECT:
                return self.code[self.code[pos]]
            case MODE.IMMEDIATE:
                return self.code[pos]

    def resume(self):
        self.state = State.READY
        self.run_until_end()

    def run_until_end(self) -> "IntCode":
        while self.code[self.pc] != 99:
            instr = self.code[self.pc]
            op = OP(instr % 100)
            mode_1 = MODE(instr // 100 % 10)
            mode_2 = MODE(instr // 1_000 % 10)
            mode_3 = MODE(instr // 10_000 % 10)

            match op:
                case OP.ADD:
                    p1 = self.get_param(self.pc + 1, mode_1)
                    p2 = self.get_param(self.pc + 2, mode_2)
                    if mode_3 == MODE.INDIRECT:
                        self.code[self.code[self.pc + 3]] = p1 + p2
                    else:
                        raise NotImplementedError
                    self.pc += 4
                case OP.MUL:
                    p1 = self.get_param(self.pc + 1, mode_1)
                    p2 = self.get_param(self.pc + 2, mode_2)
                    if mode_3 == MODE.INDIRECT:
                        self.code[self.code[self.pc + 3]] = p1 * p2
                    else:
                        raise NotImplementedError
                    self.pc += 4
                case OP.NZJMP:
                    p1 = self.get_param(self.pc + 1, mode_1)
                    p2 = self.get_param(self.pc + 2, mode_2)
                    self.pc += 3
                    if p1 != 0:
                        self.pc = p2
                case OP.ZJMP:
                    p1 = self.get_param(self.pc + 1, mode_1)
                    p2 = self.get_param(self.pc + 2, mode_2)
                    self.pc += 3
                    if p1 == 0:
                        self.pc = p2
                case OP.LT:
                    p1 = self.get_param(self.pc + 1, mode_1)
                    p2 = self.get_param(self.pc + 2, mode_2)
                    if mode_3 == MODE.INDIRECT:
                        self.code[self.code[self.pc + 3]] = int(p1 < p2)
                    else:
                        raise NotImplementedError
                    self.pc += 4

                case OP.EQ:
                    p1 = self.get_param(self.pc + 1, mode_1)
                    p2 = self.get_param(self.pc + 2, mode_2)
                    if mode_3 == MODE.INDIRECT:
                        self.code[self.code[self.pc + 3]] = int(p1 == p2)
                    else:
                        raise NotImplementedError
                    self.pc += 4

                case OP.INPUT:
                    if not self.inp:
                        self.state = State.WAIT_INPUT
                        break
                    if mode_1 == MODE.INDIRECT:
                        self.code[self.code[self.pc + 1]] = self.inp.popleft()
                    else:
                        raise NotImplementedError
                    self.pc += 2
                case OP.OUTPUT:
                    self.state = State.WAIT_OUTPUT
                    p1 = self.get_param(self.pc + 1, mode_1)
                    self.output.append(p1)
                    self.pc += 2
                    break
                case _:
                    raise NotImplementedError
        return self
