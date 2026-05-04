# Total action space = 8*8*8*8 = 4096

def encode_move(move):
    (x1, y1), (x2, y2) = move
    return ((x1 * 8 + y1) * 64) + (x2 * 8 + y2)


def decode_move(action):
    start = action // 64
    end = action % 64

    x1 = start // 8
    y1 = start % 8

    x2 = end // 8
    y2 = end % 8

    return ((x1, y1), (x2, y2))