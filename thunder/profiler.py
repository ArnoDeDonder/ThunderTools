from collections import defaultdict
from time import time
from typing import Dict, DefaultDict, Callable, Optional
import atexit
import functools


class Profiler:
    def __init__(self, auto_report: bool = True) -> None:
        self.profiles: DefaultDict[str, Dict[str, float]] = defaultdict(lambda: {'count': 0, 'total_time': 0})
        self.active_profiles: Dict[str, float] = {}
        self.auto_report = auto_report
        if self.auto_report:
            atexit.register(self.report)

    def __enter__(self) -> 'Profiler':
        self.start('_global')
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb) -> None:
        self.stop('_global')
        if self.auto_report:
            self.report()

    def _format_time(self, duration_seconds: float) -> str:
        # Using more readable format for time duration
        hours, remainder = divmod(duration_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = (duration_seconds % 1) * 1000
        return f"{int(hours):02d}h {int(minutes):02d}m {int(seconds):02d}s {int(milliseconds):03d}ms"

    def start(self, name: str) -> None:
        if name in self.active_profiles:
            raise ValueError(f"Profile '{name}' is already running.")
        self.active_profiles[name] = time()

    def stop(self, name: str) -> None:
        start_time = self.active_profiles.pop(name, None)
        if start_time is None:
            raise ValueError(f"Profile '{name}' has not been started.")
        duration = time() - start_time
        self.profiles[name]['count'] += 1
        self.profiles[name]['total_time'] += duration

    def report(self) -> None:
        output = '[Profiling Results]\n'
        max_profile_len = max((len(profile) for profile in self.profiles), default=0)
        for profile, data in sorted(self.profiles.items(), key=lambda item: item[1]['total_time'], reverse=True):
            average_time = data['total_time'] / data['count'] if data['count'] > 0 else 0
            output += f"{profile.ljust(max_profile_len + 2)} Avg: {self._format_time(average_time)} (Total: {self._format_time(data['total_time'])}, Count: {data['count']})\n"
        print(output)

    def time_this(self, function: Callable) -> Callable:
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            self.start(function.__name__)
            result = function(*args, **kwargs)
            self.stop(function.__name__)
            return result
        return wrapper
