import errno
import os


def bytes_to(n: int, formatted: bool = False):
    if formatted:
        for i in ['B', 'KB', 'MB', 'GB']:
            if n < 1024.0:
                return f'{n:3.2f}{i}'
            n /= 1024.0
        return n
    return float(f'{n / 1048576:3.2f}')


def get_bytes_from(path: str) -> int:
    try:
        with open(path, 'r') as b:
            return int(b.read())
    except FileNotFoundError:
        print(FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                                'Não foi possível encontrar os dados solicitados!'))
        return 0


class Square:
    @staticmethod
    def used_ram(formatted: bool = False, raw: bool = False):
        bytes: int = get_bytes_from('/sys/fs/cgroup/memory/memory.usage_in_bytes')
        return bytes if raw else bytes_to(bytes, formatted)

    @staticmethod
    def total_ram(formatted: bool = False, raw: bool = False):
        bytes: int = get_bytes_from('/sys/fs/cgroup/memory/memory.limit_in_bytes')
        return bytes if raw else bytes_to(bytes, formatted)

    @staticmethod
    def ram(formatted: bool = False) -> str:
        return f'{round(Square.used_ram(raw=True) / 1024 ** 2)}/{Square.total_ram(formatted)}'
