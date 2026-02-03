import time
from functools import wraps

def track_stats(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        class_name = args[0].__class__.__name__ if args else func.__name__
        rows = 0
        total_time = 0

        def counting_generator():
            nonlocal rows, total_time
            try:
                gen = func(*args, **kwargs)
                for row in gen:
                    start_time = time.perf_counter()
                    rows += 1
                    yield row
                    end_time = time.perf_counter()
                    total_time += (end_time - start_time)
            finally:
                print(f"Process: {class_name:<25} | Rows: {rows:>8} | Time: {total_time:>8.4f}s")
        return counting_generator()
    return wrapper