#!/usr/bin/env python

import sys

# constants:
BINOP = "binop"
OPERATION = "operation"
OPTIONAL_DATA = "optional_data"
IP = "ip"
SP = "sp"
DATA = "data"

# OPERATIONS
OP_POP = 0
OP_PUSH_CONST = 1
OP_PUSH_IP = 2
OP_PUSH_SP = 3
OP_LOAD = 4
OP_STORE = 5
OP_JUMP = 6
OP_NOT = 7
OP_PUTC = 8
OP_GETC = 9
OP_HALT = 10

BINOP_ADD = 0
BINOP_SUB = 1
BINOP_MUL = 2
BINOP_DIV = 3
BINOP_AND = 4
BINOP_OR = 5
BINOP_XOR = 6
BINOP_EQ = 7
BINOP_LT = 8


class Halt(Exception):
    pass


def main(task_file):
    with open(task_file, "r") as f:
        lines = f.readlines()

    values = [int(line, 16) for line in lines]
    data_size = values[0]
    image_size = values[1]

    data = [0 for x in range(data_size)]
    for i, v in enumerate(values[2:2 + image_size]):
        data[i] = v

    state = {
        IP: 0,
        SP: data_size,
        DATA: data
    }

    # interpret the instructions:
    while True:
        if state[IP] >= len(data):
            break

        current_instruction = data[state[IP]]
        state[IP] += 1
        try:
            execute(decode(current_instruction), state)
        except Halt:
            break


# functions:
def decode(instruction):
    binop_mask = 0x80000000
    operation_mask = 0x7F000000
    optional_data_mask = 0x00FFFFFF

    # extract fields from the instruction:
    binop = (instruction & binop_mask) >> 31
    operation = (instruction & operation_mask) >> 24
    optional_data = instruction & optional_data_mask

    return {
        BINOP: binop,
        OPERATION: operation,
        OPTIONAL_DATA: optional_data
    }


def execute(instruction, state):
    if instruction[BINOP]:
        execute_binary_operation(instruction, state)
    else:
        execute_operation(instruction, state)


def execute_operation(instruction, state):
    if instruction[OPERATION] == OP_POP:
        state[SP] += 1
    elif instruction[OPERATION] == OP_PUSH_CONST:
        push(state, instruction[OPTIONAL_DATA])
    elif instruction[OPERATION] == OP_PUSH_IP:
        push(state, state[IP])
    elif instruction[OPERATION] == OP_PUSH_SP:
        push(state, state[SP])
    elif instruction[OPERATION] == OP_LOAD:
        addr = pop(state)
        push(state, state[DATA][addr])
    elif instruction[OPERATION] == OP_STORE:
        store_data = pop(state)
        addr = pop(state)
        state[DATA][addr] = store_data
    elif instruction[OPERATION] == OP_JUMP:
        cond = pop(state)
        addr = pop(state)
        if cond:
            state[IP] = addr
    elif instruction[OPERATION] == OP_NOT:
        if pop(state):
            push(state, 0)
        else: 
            push(state, 1)
    elif instruction[OPERATION] == OP_PUTC:
        c = chr(pop(state) & 0xFF)
        sys.stdout.write(c)
        sys.stdout.flush()
    elif instruction[OPERATION] == OP_GETC:
        x = sys.stdin.read(1)
        x = ord(x)
        push(state, x & 0xFF)
    elif instruction[OPERATION] == OP_HALT:
        raise Halt()
    else:
        raise Exception('unknown instruction' + hex(instruction))


def execute_binary_operation(instruction, state):
    b = pop(state)
    a = pop(state)
    result = 0
    if instruction[OPERATION] == BINOP_ADD:
        result = a + b
    elif instruction[OPERATION] == BINOP_SUB:
        result = a - b
    elif instruction[OPERATION] == BINOP_MUL:
        result = a * b
    elif instruction[OPERATION] == BINOP_DIV:
        result = a / b
    elif instruction[OPERATION] == BINOP_AND:
        result = a & b
    elif instruction[OPERATION] == BINOP_OR:
        result = a | b
    elif instruction[OPERATION] == BINOP_XOR:
        result = a ^ b
    elif instruction[OPERATION] == BINOP_EQ:
        result = 1 if a == b else 0
    elif instruction[OPERATION] == BINOP_LT:
        result = 1 if a < b else 0
    else:
        raise Exception('unknown instruction' + hex(instruction))

    push(state, result)


# f(v)
def push(state, value):
    state[SP] -= 1
    state[DATA][state[SP]] = value


# g()
def pop(state):
    value = state[DATA][state[SP]]
    state[SP] += 1
    return value


if __name__ == '__main__':
    main(sys.argv[1])
