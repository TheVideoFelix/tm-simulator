import enum

class HeadMovingDirections(enum.Enum):
    N = 'N'
    R = 'R'
    L = 'L'

    @classmethod
    def from_char(cls, input: str):
        try:
             return cls(input.upper())
        except ValueError:
            return None

"""
Input: M = (Q, Σ, Γ, B, q0, ¯q, δ), 
"""
class TuringMachine: 
    def __init__(self, number_of_states: int, alphabet: list[str], tape_alphabet: list[str], start_state: str, end_state: str, transitions: list['Transition']):
        self.states: list[str] = [str(i) for i in range(1, number_of_states + 1)]
        self.alphabet = alphabet
        self.tape_alphabet = tape_alphabet
        self.end_state = end_state
        self.transitions = {transition.get_key(): transition for transition in transitions}
        
        self.tape = Tape()
        self.state = start_state

    def input(self, input: str) -> None:
        self.tape.init_tape(input)

    def step(self):
        transition = self.transitions.get(self.state + self.tape.get_head_value())
        if transition is None:
            raise ValueError(f"No transition found for state '{self.state}' and tape symbol '{self.tape.get_head_value()}'")
        self.tape.set_head_value(transition.new_tape_symbol)
        self.tape.move_head(transition.direction)
        self.state = transition.new_state
    
    def run(self):
        while self.state != self.end_state:
            print(self.current_tape_str())
            self.step()
        print(self.current_tape_str())

    def current_tape_str(self) -> str:
        left, head, right = self.tape.get_tape_representation()
        return f'...B{left}[{self.state}]{head}{right}B...'

    def __str__(self) -> str:
        return f"TuringMachine(state={self.state}, end_state={self.end_state}, tape={self.tape})"

"""
δ : (q, a)  → (q′, b, D) 
δ(q₀, (a, □)) = (q₀, (a, a), (R, R))
q, a, q′, b, D
1 0 1 1 R

"""
class Transition:
    def __init__(self, current_state: str, current_tape_symbol: str, new_state: str, new_tape_symbol: str, direction: HeadMovingDirections) -> None:
        self.current_state = current_state
        self.current_tape_symbol = current_tape_symbol
        self.new_state = new_state
        self.new_tape_symbol = new_tape_symbol
        self.direction = direction
    
    @classmethod
    def from_input_str(cls, input: str):
        inputs = input.split()
        direction = HeadMovingDirections.from_char(inputs[4])
        if not direction:
            raise ValueError('The given direction does not match on of this R,L,N')
        return cls(inputs[0], inputs[1], inputs[2], inputs[3], direction)
    
    def get_key(self) -> str:
        return self.current_state + self.current_tape_symbol



class Tape:
    def __init__(self) -> None:
        self.tape_to_left: list[str] = []
        self.tape_to_right: list[str] = []

    def init_tape(self, input: str) -> None:
        self.tape_to_right = list(reversed(list(input)))

    def move_head(self, direction: HeadMovingDirections) -> None:
        match direction:
            case HeadMovingDirections.N:
                pass
            case HeadMovingDirections.R:
                self._move_head_right()
            case HeadMovingDirections.L:
                self._move_head_left()

    def get_head_value(self) -> str:
        if self.tape_to_right:
            return self.tape_to_right[-1]
        else:
            return self.blank()
    
    def set_head_value(self, new_head_value: str) -> None:
        if self.tape_to_right:
            self.tape_to_right[-1] = new_head_value
        else:
            self.tape_to_right.append(new_head_value)
    
    def _move_head_right(self) -> None: 
        if self.tape_to_right:
            self.tape_to_left.append(self.tape_to_right.pop())
        else:
            self.tape_to_left.append(self.blank())

    def _move_head_left(self) -> None:
        if self.tape_to_left:
            self.tape_to_right.append(self.tape_to_left.pop())
        else:
            self.tape_to_right.append(self.blank())

    def get_tape_representation(self) -> tuple[str, str, str]:
        left_str = "".join(self.tape_to_left)
        if not self.tape_to_right:
            head_char = self.blank()
            right_str = ""
        else:
            head_char = self.tape_to_right[-1]
            right_part_list = self.tape_to_right[:-1]
            right_part_list.reverse()
            right_str = "".join(right_part_list)
        return left_str, head_char, right_str

    @staticmethod
    def blank() -> str:
        return 'B'

    def __str__(self) -> str:
        left, head, right = self.get_tape_representation()
        return f'...B{left}[{head}]{right}B...'
    