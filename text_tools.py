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


def merge_text_blocks(b1: str, b2: str) -> str:
    b1_list = b1.split('\n')
    b2_list = b2.split('\n')

    if len(b1_list) < len(b2_list):
        for ii in range(len(b2_list) - len(b1_list)):
            b1_list.append("")

    text_block = ""

    for ii in range(len(b1_list)):
        text_block += b1_list[ii]
        if(ii < len(b2_list)):
            text_block += b2_list[ii]
        text_block += "\n"
    
    return text_block