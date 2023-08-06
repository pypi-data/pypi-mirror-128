import os.path as path
import os
import pdfkit


def folderPath(initialDirectory):
    # this function fixes the given directory path of the user
    finalDirectory = ""
    # duplicate \ of the directory
    for char in initialDirectory:
        if char == "\\":
            finalDirectory += char + char
        else:
            finalDirectory += char

    # join the directory with the filename
    return finalDirectory


def ntkBake(fileName, content, exportTo=None, directory=None):
    fileNameType = fileName + ".html"

    if directory is None or directory == 0:
        fileNameTypePDF = fileName + ".pdf"

        if exportTo is None or exportTo == 0:
            # run default, export to both html and pdf
            with open(fileNameType, "w") as f:
                f.write(content)
            pdfkit.from_file(fileNameType, fileNameTypePDF)
        else:
            if exportTo == 1:
                # export to html only
                with open(fileNameType, "w") as f:
                    f.write(content)
            else:
                # run default, export to both html and pdf
                with open(fileNameType, "w") as f:
                    f.write(content)
                pdfkit.from_file(fileNameType, fileNameTypePDF)

    else:

        # if the user gave a directory, use this
        finalDirectory = folderPath(directory)

        # comepleteFileName of .html file
        completeFileName = path.join(finalDirectory, fileNameType)

        fileNameTypePDF = fileName + ".pdf"

        # completeFileName of .pdf file
        completeFileNamePDF = path.join(finalDirectory, fileNameTypePDF)

        if exportTo is None or exportTo == 0:
            # run default, export to both html and pdf
            with open(completeFileName, "w") as f:
                f.write(content)
            pdfkit.from_file(completeFileName, completeFileNamePDF)
        else:
            if exportTo == 1:
                # export to html only
                with open(completeFileName, "w") as f:
                    f.write(content)
            else:
                # run default, export to both html and pdf
                with open(completeFileName, "w") as f:
                    f.write(content)
                pdfkit.from_file(completeFileName, completeFileNamePDF)
