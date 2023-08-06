from enum import Enum
from typing import Optional, Union, List
from weakref import ref


def suffix(suffix: str, condition: bool) -> str:
    if condition:
        return suffix
    return ''


class Operand:
    def __bool__(self):
        return False

    def __repr__(self):
        return str(self)


class Register(Operand):
    number: int

    def __init__(self, text: str):
        if text.startswith('r'):
            self.number = int(text[1:])
        elif text == 'sb':
            self.number = 9
        elif text == 'sl':
            self.number = 10
        elif text == 'ip':
            self.number = 12
        elif text == 'sp':
            self.number = 13
        elif text == 'lr':
            self.number = 14
        elif text == 'pc':
            self.number = 15
        else:
            raise ValueError(f'bad register {text}')

    def __repr__(self):
        if self.number <= 12:
            return f'r{self.number}'
        if self.number == 13:
            return 'sp'
        if self.number == 14:
            return 'lr'
        if self.number == 15:
            return 'pc'

    def __eq__(self, other):
        if isinstance(other, Register):
            return self.number == other.number
        return False

    def __bool__(self):
        return True


class Constant(Operand):
    value: int

    def __init__(self, value: Union[str, int]):
        if isinstance(value, str):
            self.value = int(value, 0)
        else:
            self.value = value

    def __repr__(self):
        return f'#{self.value:#x}'

    def __eq__(self, other):
        if isinstance(other, Constant):
            return self.value == other.value
        return False

    def __bool__(self):
        return self.value != 0


class ASTNode:
    pass


class Instruction(ASTNode):
    _prev: Optional[ref] = None
    _next: Optional[ref] = None

    @property
    def prev(self) -> Optional['Instruction']:
        if self._prev:
            return self._prev()
        return None

    @property
    def next(self) -> Optional['Instruction']:
        if self._next:
            return self._next()
        return None


class Operation(Instruction):
    rd: Register
    rn: Register
    rm: Operand
    mnemonic: str

    def __init__(self, rd: Register, rn: Register, rm: Operand):
        self.rd = rd
        self.rn = rn
        self.rm = rm

    def __repr__(self):
        if self.rd == self.rn:
            return f'{self.mnemonic} {self.rd}, {self.rm}'
        return f'{self.mnemonic} {self.rd}, {self.rn}, {self.rm}'


class LabelType(Enum):
    CODE = 0
    DATA = 1
    CASE = 2
    OTHER = 3


class LABEL(Instruction):
    name: str
    type: LabelType
    loads: List['LDR_PC']

    def __init__(self, name: str):
        self.name = name
        self.type = LabelType.OTHER
        self.loads = []

    def __repr__(self):
        return f'{self.name}:'


class DATA(Instruction):
    size: int
    data: Union[str, int]
    offset: Optional[int]
    _target: Optional[ref]

    def __init__(self, size: int, data: Union[str, int], offset: Optional[int] = None):
        self.size = size
        self.data = data
        self.offset = offset
        self._target = None

    @property
    def target(self) -> Optional[LABEL]:
        if self._target:
            return self._target()
        return None

    def __repr__(self):
        if self.target:
            return f'.{self.size}byte {self.target.name}'
        if isinstance(self.data, int):
            return f'.{self.size}byte {self.data:#x}'
        r = f'.{self.size}byte {self.data}'
        if self.offset:
            r += f'+{self.offset:#x}'
        return r


class PUSH(Instruction):
    registers: List[Register]

    def __init__(self, registers: List[Register]):
        self.registers = registers

    def __repr__(self):
        return f'push {{{", ".join([str(reg) for reg in self.registers])}}}'


class POP(Instruction):
    registers: List[Register]

    def __init__(self, registers: List[Register]):
        self.registers = registers

    def __repr__(self):
        return f'pop {{{", ".join([str(reg) for reg in self.registers])}}}'


class ADD(Operation):
    mnemonic = 'add'


class SUB(Operation):
    mnemonic = 'sub'


class NEG(Instruction):
    rd: Register
    rm: Register

    def __init__(self, rd: Register, rm: Register):
        self.rd = rd
        self.rm = rm

    def __repr__(self):
        return f'neg {self.rd}, {self.rm}'


class MUL(Instruction):
    rd: Register
    rn: Register
    rm: Register

    def __init__(self, rd: Register, rn: Register, rm: Register):
        if not (rd == rn or rd == rm):
            raise ValueError('mul destination must be equal to one of the factors')
        self.rd = rd
        self.rn = rn
        self.rm = rm

    def __repr__(self):
        if self.rd == self.rn:
            return f'mul {self.rd}, {self.rm}'
        if self.rd == self.rm:
            return f'mul {self.rd}, {self.rn}'
        return f'mul {self.rd}, {self.rn}, {self.rm}'


class AND(Operation):
    mnemonic = 'and'


class ORR(Operation):
    mnemonic = 'orr'


class EOR(Operation):
    mnemonic = 'eor'


class LSL(Operation):
    mnemonic = 'lsl'


class LSR(Operation):
    mnemonic = 'lsr'


class ASL(Operation):
    mnemonic = 'asl'


class ASR(Operation):
    mnemonic = 'asr'


class BIC(Operation):
    mnemonic = 'bic'


class LDR_PC(Instruction):
    rt: Register
    _label: str
    offset: int = 0
    size: int = 4
    signed: bool = False
    _target: Optional[ref]

    def __init__(self, rt: Register, label: str, offset: int = 0, size: int = 4, signed: bool = False):
        self.rt = rt
        self._label = label
        self.offset = offset
        self.size = size
        self.signed = signed
        self._target = None

    @property
    def target(self) -> Optional[LABEL]:
        if self._target:
            return self._target()
        return None

    @property
    def label(self) -> str:
        if self.target:
            return self.target.name
        return self._label

    def __repr__(self):
        text = f'ldr{suffix("s", self.signed)}{suffix("b", self.size == 1)}{suffix("h", self.size == 2)} {self.rt}, {self.label}'
        if self.offset != 0:
            text += f'+{self.offset:#x}'
        return text


class LDR(Instruction):
    rt: Register
    rn: Register
    rm: Optional[Operand]
    size: int = 4
    signed: bool = False

    def __init__(self, rt: Register, rn: Register, rm: Optional[Operand], size: int = 4, signed: bool = False):
        self.rt = rt
        self.rn = rn
        self.rm = rm
        self.size = size
        self.signed = signed

    def __repr__(self):
        return f'ldr{suffix("s", self.signed)}{suffix("b", self.size == 1)}{suffix("h", self.size == 2)} {self.rt}, ' \
               f'[{self.rn}{suffix(", ", self.rm)}{suffix(str(self.rm), self.rm)}]'


class STR(Instruction):
    rt: Register
    rn: Register
    rm: Optional[Operand]
    size: int = 4

    def __init__(self, rt: Register, rn: Register, rm: Optional[Operand], size: int = 4):
        self.rt = rt
        self.rn = rn
        self.rm = rm
        self.size = size

    def __repr__(self):
        return f'str{suffix("b", self.size == 1)}{suffix("h", self.size == 2)} {self.rt}, ' \
               f'[{self.rn}{suffix(", ", self.rm)}{suffix(str(self.rm), self.rm)}]'


class STM(Instruction):
    rn: Register
    reglist: List[Register]

    def __init__(self, rn: Register, reglist: List[Register]):
        self.rn = rn
        self.reglist = reglist

    def __repr__(self):
        return f'stm {self.rn}!, {{{", ".join([str(reg) for reg in self.reglist])}}}'


class BL(Instruction):
    function: str

    def __init__(self, function: str):
        self.function = function

    def __repr__(self):
        return f'bl {self.function}'


class BX(Instruction):
    rm: Register

    def __init__(self, rm: Register):
        self.rm = rm

    def __repr__(self):
        return f'bx {self.rm}'


class Branch(Instruction):
    _label: str
    condition: str
    _target: Optional[ref]

    def __init__(self, label: str):
        self._label = label
        self._target = None

    @property
    def target(self) -> Optional[LABEL]:
        if self._target:
            return self._target()
        return None

    @property
    def label(self):
        if self.target:
            return self.target.name
        return self._label

    def __repr__(self):
        return f'b{self.condition} {self.label}'


class B(Branch):
    condition = ''


class BEQ(Branch):
    condition = 'eq'


class BNE(Branch):
    condition = 'ne'


class BHS(Branch):
    condition = 'hs'


class BLO(Branch):
    condition = 'lo'


class BMI(Branch):
    condition = 'mi'


class BPL(Branch):
    condition = 'pl'


class BVS(Branch):
    condition = 'vs'


class BVC(Branch):
    condition = 'vc'


class BHI(Branch):
    condition = 'hi'


class BLS(Branch):
    condition = 'ls'


class BGE(Branch):
    condition = 'ge'


class BLT(Branch):
    condition = 'lt'


class BGT(Branch):
    condition = 'gt'


class BLE(Branch):
    condition = 'le'


class CMP(Instruction):
    rn: Register
    rm: Operand

    def __init__(self, rn: Register, rm: Register):
        self.rn = rn
        self.rm = rm

    def __repr__(self):
        return f'cmp {self.rn}, {self.rm}'


class CMN(Instruction):
    rn: Register
    rm: Operand

    def __init__(self, rn: Register, rm: Register):
        self.rn = rn
        self.rm = rm

    def __repr__(self):
        return f'cmn {self.rn}, {self.rm}'


class MOV(Instruction):
    rd: Register
    rm: Operand

    def __init__(self, rd: Register, rm: Register):
        self.rd = rd
        self.rm = rm

    def __repr__(self):
        return f'mov {self.rd}, {self.rm}'


class MVN(Instruction):
    rd: Register
    rm: Operand

    def __init__(self, rd: Register, rm: Register):
        self.rd = rd
        self.rm = rm

    def __repr__(self):
        return f'mvn {self.rd}, {self.rm}'


class Directive(Instruction):
    text: str

    def __init__(self, text: str):
        self.text = text

    def __repr__(self):
        return self.text


class FileDirective(Directive):
    id: int
    path: str

    def __init__(self, id: int, path: str):
        super().__init__(f'.file {id} "{path}"')
        self.id = id
        self.path = path


class LocDirective(Directive):
    file: int
    line: int
    column: int

    def __init__(self, file: int, line: int, column: int):
        super().__init__(f'.loc {file} {line} {column}')
        self.file = file
        self.line = line
        self.column = column


class Function(ASTNode):
    name: str
    instructions: List[Instruction]
    labels: List[LABEL]

    def __init__(self, name: str, instructions: List[Instruction]):
        self.name = name
        self.instructions = instructions
        self.labels = []


class ASMFile(ASTNode):
    functions: List[Function]

    def __init__(self, functions: List[Function]):
        self.functions = functions
