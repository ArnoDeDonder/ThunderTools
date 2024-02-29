from datetime import datetime
from time import time
from typing import Iterable
from statistics import mean

BLOCK_SYMBOL = '█'
NON_BLOCK_SYMBOL = '░'


def _format_seconds_to_hms(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "{:02d}:{:02d}:{:02d}".format(int(h), int(m), int(round(s)))


def citer(items: Iterable, block_amount=50, iterator_log_interval=100):  # Count ITERation
    start_time = time()
    iteration_durations = []
    try:
        len(items)
    except TypeError:
        for i, item in enumerate(items):
            if i > 0 and i % iterator_log_interval == 0:
                print(f'({i} / ?)')
            yield item
        return
    item_amount = len(list(items))
    if item_amount == 0:
        return
    for i, item in enumerate(items):
        iteration_start_time = time()
        if i > 0 and i % (int(item_amount / block_amount) or 1) == 0:
            block_to_print = int(round(i / item_amount * block_amount, 0))
            non_blocks_to_print = block_amount - block_to_print
            total_iteration_time = (mean(iteration_durations) * item_amount)
            time_elapsed = time() - start_time
            print(
                f'({str(i).ljust(len(str(item_amount)))} / {item_amount}) : '
                + block_to_print * BLOCK_SYMBOL + non_blocks_to_print * NON_BLOCK_SYMBOL
                + f' - ETA: {"∞" if not iteration_durations else (datetime.fromtimestamp(start_time + total_iteration_time)).replace(microsecond=0)}'
                + f' [{_format_seconds_to_hms(time_elapsed)}<{_format_seconds_to_hms(total_iteration_time)}]'
            )
        yield item
        iteration_durations.append(time() - iteration_start_time)