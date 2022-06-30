def add_bar(msg: str, loc: str)->str:

    filler = "-" * get_text_block_width(msg)
    if loc=="below":
        msg = msg + '\n' + filler + '\n'
    elif loc=="above":
        msg = filler + '\n' +  msg + '\n'

    else:
        msg = msg + '\n' + filler + '\n'


    return msg

def get_text_block_width(msg:str)->int:

    lines = msg.split('\n')
    print(lines)

    line_lens = [len(line) for line in lines]

    return max(line_lens)