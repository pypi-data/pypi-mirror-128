#      (canch, write_id, read_id)

def get_board_id(board):
    boards = {
        #board_num: {canch, write_id, read_id}
        0: {"canch": 1, "write_id": 0x07, "read_id": 0x08},
        # 1: {"canch": 1, "write_id": 0x07, "read_id": 0x08},
        # 2: {"canch": 1, "write_id": 0x03, "read_id": 0x04} #test_mode
    }

    return boards[board]
