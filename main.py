import sys
import os
import logging
from tm import Tape, Transition, TuringMachine as TM, MultiTapeTuringMachine as MTTM

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main() -> int:
    args = sys.argv
    args_len = len(args)

    if args_len != 3:
        logging.error('Usage: python %s <path_to_file.TM|MTTM> <TM input>', args[0])
        logging.error('Please provide exactly one file path as an argument')
        return 1
    
    file_path = args[1]
    print(file_path)
    
    if not file_path.endswith(('.TM', '.MTTM')):
        logging.error('The provided file is not a .TM or .MTTM file.')
        return 1
    
    file_lines = read_file(file_path)

    if not file_lines:
        logging.error('Could not read file or file is empty.')
        return 1

    if len(file_lines) < 5:
        logging.error('File is not in the correct format, please check your file again.')
        return 1
    
    file_lines.reverse()

    tapes = 1

    if file_path.endswith('.MTTM'):
        tapes = int(file_lines.pop())

    states = int(file_lines.pop())
    alphabet = list(file_lines.pop())
    tape_alphabet = list(file_lines.pop())

    if not Tape.blank() in tape_alphabet:
        logging.warning('The tape alpahabet does not contain the blank symbole')

    start_state = file_lines.pop()
    end_state = file_lines.pop()

    if not file_lines:
        logging.error('The TM does not have any transtions.')
        return 1

    try:
        transitions = [Transition.from_input_str(s) for s in file_lines]
    except ValueError as e:
        logging.error(e)
        return 1

    turing_machine_input = args[2].split(',')

    if tapes > 1:
        turing_machine = MTTM(tapes, states, alphabet, tape_alphabet, start_state, end_state, transitions) 
    else:
        turing_machine = TM(states, alphabet, tape_alphabet, start_state, end_state, transitions)


    turing_machine.input(turing_machine_input)

    try:
        turing_machine.run()
    except ValueError as e:
        logging.error(e)
        return 1

    return 0

def read_file(file_path: str) -> list[str]:
    if not os.path.exists(file_path):
        logging.error(f"The file '{file_path}' couldn't be found.")
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
        return lines
    except Exception as e:
        logging.error(f'An error occurred by ready the file: {e}')
        return []

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)