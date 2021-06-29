def convert_codec(sourceFileName, targetFileName):
    import codecs
    BLOCKSIZE = 1048576 # or some other, desired size in bytes
    with codecs.open(sourceFileName, "r", "cp1252") as sourceFile:
        with codecs.open(targetFileName, "w", "utf-8") as targetFile:
            while True:
                contents = sourceFile.read(BLOCKSIZE)
                if not contents:
                    break
                targetFile.write(contents)
