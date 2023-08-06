from robertcommon.system.io.file import FileType, FileConfig, FileAccessor

def test_csv():
    accessor = FileAccessor(FileConfig(PATH='', MODE=FileType.CSV))
    accessor.save('')