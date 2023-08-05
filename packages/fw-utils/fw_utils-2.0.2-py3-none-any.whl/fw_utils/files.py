"""Binary-, temporary and globbing file helpers."""
import os
import typing as t
from pathlib import Path
from tempfile import SpooledTemporaryFile, TemporaryDirectory

from .parsers import parse_hrsize

__all__ = [
    "AnyPath",
    "AnyFile",
    "BinFile",
    "TempDir",
    "TempFile",
    "fileglob",
    "open_any",
]


class BinFile:
    """Wrapper for accessing local paths and file-like objects similarly."""

    def __init__(
        self,
        file: t.Union[str, Path, t.IO],
        mode: str = "rb",
        metapath: str = "",
    ) -> None:
        """Open a file for reading or writing.

        Args:
            file (str|Path|file): The local path to open or a file-like object.
            mode (str, optional): The file opening mode, rb|wb. Default: rb.
            metapath (str, optional): Override metapath attribute if given.
        """
        if mode not in {"rb", "wb"}:
            raise ValueError(f"Invalid file mode: {mode} (expected rb|wb)")
        self.file: t.IO = None  # type: ignore
        self.file_open = False
        self.localpath = None
        self.mode = mode
        mode_func = "readable" if mode == "rb" else "writable"
        if isinstance(file, (str, Path)):
            self.file_open = True
            self.localpath = str(Path(file).resolve())
            # pylint: disable=unspecified-encoding
            file = Path(self.localpath).open(mode=mode)
        if not hasattr(file, mode_func) or not getattr(file, mode_func)():
            raise ValueError(f"File {file!r} is not {mode_func}")
        self.file = file
        self.metapath = metapath or self.localpath

    def __getattr__(self, name: str):
        """Return attrs proxied from the file."""
        return getattr(self.file, name)

    def __iter__(self):
        """Iterate over lines."""
        return self.file.__iter__()

    def __next__(self):
        """Get next line."""
        return self.file.__next__()

    def __enter__(self) -> "BinFile":
        """Enter 'with' context - seek to start if it's a BinaryIO or a TempFile."""
        if self.file.seekable():
            self.file.seek(0)
        return self

    def __exit__(self, exc_cls, exc_val, exc_trace) -> None:
        """Exit 'with' context - close file if it was opened by BinFile."""
        if self.file_open:
            self.file.close()

    def __repr__(self) -> str:
        """Return string representation of the BinFile."""
        file_str = self.metapath or f"{type(self.file).__name__}/{hex(id(self.file))}"
        return f"{type(self).__name__}('{file_str}', mode='{self.mode}')"


# unified type for strings and paths
AnyPath = t.Union[str, Path]
# unified type for paths and file-like objects
AnyFile = t.Union[str, Path, t.IO, BinFile]


class TempDir(TemporaryDirectory):
    """Temporary directory with chdir support."""

    def __init__(self, chdir: bool = False, **kwargs) -> None:
        """Initialize TempDir."""
        super().__init__(**kwargs)
        self.chdir = chdir
        self.cwd = os.getcwd()

    def __enter__(self) -> Path:
        """Return tempdir (and optionally chdir) when entering the context."""
        if self.chdir:
            os.chdir(self.name)
        return Path(self.name)

    def __exit__(self, exc, value, tb) -> None:
        """Restore the CWD if needed when exiting the context."""
        if self.chdir:
            os.chdir(self.cwd)
        self.cleanup()


FW_SPOOL_SIZE = "10MB"


class TempFile(SpooledTemporaryFile):
    """Spooled tempfile with read/write/seekable() methods and default max size."""

    _file: t.IO

    def __init__(self, **kwargs) -> None:
        """Initialize TempFile with default max size."""
        if "max_size" not in kwargs:
            max_size = parse_hrsize(os.getenv("FW_SPOOL_SIZE", FW_SPOOL_SIZE))
            kwargs["max_size"] = max_size
        super().__init__(**kwargs)

    def readable(self) -> bool:
        """Return that the file is readable."""
        return self._file.readable()

    def writable(self) -> bool:
        """Return that the file is writable."""
        return self._file.writable()

    def seekable(self) -> bool:
        """Return that the file is seekable."""
        return self._file.seekable()


def fileglob(
    dirpath: AnyPath,
    pattern: str = "*",
    recurse: bool = False,
) -> t.List[Path]:
    """Return the list of files under a given directory.

    Args:
        dirpath (str|Path): The directory path to glob in.
        pattern (str, optional): The glob pattern to match files on. Default: "*".
        recurse (bool, optional): Toggle for enabling recursion. Default: False.

    Returns:
        list[Path]: The file paths that matched the glob within the directory.
    """
    if isinstance(dirpath, str):
        dirpath = Path(dirpath)
    glob_fn = getattr(dirpath, "rglob" if recurse else "glob")
    return list(sorted(f for f in glob_fn(pattern) if f.is_file()))


def open_any(file: AnyFile, mode: str = "rb") -> BinFile:
    """Return BinFile object as-is or AnyFile loaded as BinFile."""
    if isinstance(file, BinFile):
        if mode != file.mode:
            raise ValueError(f"open_any {mode!r} on a {file.mode!r} BinFile")
        return file
    return BinFile(file, mode=mode)
