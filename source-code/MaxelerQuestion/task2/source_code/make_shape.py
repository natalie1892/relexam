#!/usr/bin/env python

# state consts:
RIGHT_PAD_COUNT = "right_pad_count"

# orientation consts
EAST = "E"
WEST = "W"
NORTH = "N"
SOUTH = "S"

PAD = "P"


# basic shape: DRURDRUR
# orientation: N, W, S, E. the basic shape is with orientation E
# flip: defines whether the orientation should also be flipped

def draw_shape(scale, orientation, flip=False):
    if orientation == EAST and not flip:
        v1, v2, v3, u = "DRUL"
    elif orientation == EAST and flip:
        v1, v2, v3, u = "URDL"
    elif orientation == NORTH and not flip:
        v1, v2, v3, u = "RDLU"
    elif orientation == NORTH and flip:
        v1, v2, v3, u = "LDRU"
    elif orientation == WEST and not flip:
        v1, v2, v3, u = "DLUR"
    elif orientation == WEST and flip:
        v1, v2, v3, u = "ULDR"
    elif orientation == SOUTH and not flip:
        v1, v2, v3, u = "RULD"
    elif orientation == SOUTH and flip:
        v1, v2, v3, u = "LURD"

    else:
        raise Exception("invalid argument " + str(orientation))

    shape = v1 + v2 + v3 + v2 + v1 + v2 + v3 + v2
    undo_shape = PAD + (4 * str(u)) + PAD

    if scale >= 0:
        scaling_string = scale * "NK"
        descaling_string = scale * "MJ"
    else:
        scaling_string = -scale * "MJ"
        descaling_string = -scale * "NK"

    print(scaling_string +
          shape +
          undo_shape +
          descaling_string)


def pad(state, right, down):
    string_to_print = right * "R" + down * "U"
    string_to_print = PAD + string_to_print + PAD
    print(string_to_print)
    state[RIGHT_PAD_COUNT] += right


def return_to_beginning_of_line(state):
    string_to_print = state[RIGHT_PAD_COUNT] * "L"
    string_to_print = PAD + string_to_print + PAD
    state[RIGHT_PAD_COUNT] = 0
    print(string_to_print)


def main():
    state = {
        RIGHT_PAD_COUNT: 0,
    }

    draw_shape(0, SOUTH)
    pad(state, 40, 0)
    draw_shape(0, SOUTH, flip=True)

    return_to_beginning_of_line(state)
    pad(state, 18, 4)
    draw_shape(0, EAST)

    return_to_beginning_of_line(state)
    pad(state, 10, 3)
    draw_shape(0, EAST)
    pad(state, 20, 0)
    draw_shape(0, WEST)

    return_to_beginning_of_line(state)
    pad(state, 5, 5)
    draw_shape(0, EAST)
    pad(state, 30, 0)
    draw_shape(0, WEST)
    return_to_beginning_of_line(state)
    pad(state, 14, 4)
    draw_shape(30, EAST)

    return_to_beginning_of_line(state)
    pad(state, 3, 4)
    draw_shape(0, EAST)
    pad(state, 34, 0)
    draw_shape(0, WEST)
    return_to_beginning_of_line(state)
    pad(state, 16, 1)
    draw_shape(18, EAST)

    return_to_beginning_of_line(state)
    pad(state, 17, 4)
    draw_shape(10, EAST)
    pad(state, 1, 2)
    draw_shape(0, EAST)

    return_to_beginning_of_line(state)
    pad(state, 5, 1)
    draw_shape(0, EAST, flip=True)
    pad(state, 30, 0)
    draw_shape(0, WEST, flip=True)
    return_to_beginning_of_line(state)
    pad(state, 19, 1)
    draw_shape(-4, EAST)

    return_to_beginning_of_line(state)
    pad(state, 10, 3)
    draw_shape(0, EAST, flip=True)
    pad(state, 20, 0)
    draw_shape(0, WEST, flip=True)

    return_to_beginning_of_line(state)
    pad(state, 18, 4)
    draw_shape(0, EAST)

    return_to_beginning_of_line(state)
    draw_shape(0, SOUTH)
    pad(state, 40, 0)
    draw_shape(0, SOUTH, flip=True)

    print("X")


if __name__ == "__main__":
    main()
