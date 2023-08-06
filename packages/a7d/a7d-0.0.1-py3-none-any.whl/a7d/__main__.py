import a7d
import sys
import pathlib

source, target = map(pathlib.Path, sys.argv[1:3])
archive = a7d.Archive(source)
archive.to_directory(target) if source.is_file() else archive.save(target)
