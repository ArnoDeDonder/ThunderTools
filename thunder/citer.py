from typing import Iterable

BLOCK_SYMBOL = '█'
NON_BLOCK_SYMBOL = '░'


def citer(items: Iterable, block_amount=50, iterator_log_interval=100):  # Count ITERation
    try:
        len(items)
    except TypeError:
        for i, item in enumerate(items):
            if i > 0 and i % iterator_log_interval == 0:
                print(f'({i} / ?)')
            yield item
        return
    if (item_amount := len(list(items))) == 0:
        return
    for i, item in enumerate(items):
        if i > 0 and i % (int(item_amount / block_amount) or 1) == 0:
            block_to_print = int(round(i / item_amount * block_amount, 0))
            non_blocks_to_print = block_amount - block_to_print
            print(f'({str(i).ljust(len(str(item_amount)))} / {item_amount}) : '
                  + block_to_print * BLOCK_SYMBOL + non_blocks_to_print * NON_BLOCK_SYMBOL)
        yield item
