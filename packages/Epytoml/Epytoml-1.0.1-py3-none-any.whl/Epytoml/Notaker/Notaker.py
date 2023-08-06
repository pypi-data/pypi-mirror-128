# Epytomil, Notaker
# Created by: Zhean Ganituen

# TODO: Add Author, Date Created in ntkGen after ntkHeader

# REMEMBER: Change version number in ntkGen() function
# REMEMBER: To add a '\n' at the end of each line that is appended in the ntkTitleHead

# variable that stores all of the content of the Notaker file being created


epyCONTENT = ""

# these variables are the variables for the Notaker file being created
# _toc and _main are separated because _toc has to come first but the headers must be complete once it is generated
epyCONTENT_ntkGen = ""
epyCONTENT_ntkShut = ""
epyCONTENT_toc = ""
epyCONTENT_main = ""

# variable that counts how many header 1s are created
headCount = 1


# variable that collects all the headerCounts and their corresponding text in a key
heads = {}

# variable that collects all the links of the headers, to be used in the table of contents
links = {}


def ntkGen(fileName):
    # ntkFile is the output of the Notaker, append all user inputs here.
    global finalFileName
    global NotakerName
    NotakerName = fileName
    finalFileName = fileName + ".html"

    #'<title>fileName</title>\n'
    ntkTitle = "<title>" + fileName + "</title>\n"
    ntkTitleHead = "<h1><b>" + fileName + "</b></h1>\n"

    # write the beginning of an html document
    # <!DOCTYPE html>
    # <html lang="en">
    # <head>
    # <meta charset="UTF-8">
    # <meta http-equiv="X-UA-Compatible" content="IE=edge">
    # <meta name="viewport" content="width=device-width, initial-scale=1.0">
    # <title>Document</title>
    # </head>
    # <body>

    global epyCONTENT_ntkGen
    epyCONTENT_ntkGen += "<!DOCTYPE html>\n"
    epyCONTENT_ntkGen += '<html lang="en">\n'
    epyCONTENT_ntkGen += "<head>\n"
    epyCONTENT_ntkGen += '<meta charset="UTF-8">\n'
    epyCONTENT_ntkGen += '<meta http-equiv="X-UA-Compatible" content="IE=edge">\n'
    epyCONTENT_ntkGen += (
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    )
    epyCONTENT_ntkGen += ntkTitle
    epyCONTENT_ntkGen += "</head>\n"
    epyCONTENT_ntkGen += "<body>\n"
    epyCONTENT_ntkGen += "<!-- Created with Epytoml and Notaker. Version 1.0 --> \n"
    epyCONTENT_ntkGen += "<!-- Notaker Start --> \n"
    epyCONTENT_ntkGen += ntkTitleHead


def ntkShut():
    # write the end of an html document
    # </body>
    # </html>

    global epyCONTENT_ntkGen
    global epyCONTENT_toc
    global epyCONTENT_main
    global epyCONTENT_ntkShut

    epyCONTENT_ntkShut += "<!-- Notaker End -->\n"
    epyCONTENT_ntkShut += "</body>\n"
    epyCONTENT_ntkShut += "</html>\n"

    # append all the content to the epyCONTENT variable
    global epyCONTENT
    epyCONTENT += (
        epyCONTENT_ntkGen
        + "\n"
        + epyCONTENT_toc
        + "\n"
        + epyCONTENT_main
        + "\n"
        + epyCONTENT_ntkShut
        + "\n"
    )


def h1(text):
    # Make a header with the given text
    ntkHeader1 = "<h1>" + text + "</h1>\n"

    # Make a link id to the said header, to be used in the table of contents
    ntkID = '<a id="' + text + '"></a>\n'

    # Add the header to the heads dictionary
    heads[headCount] = ntkHeader1

    global epyCONTENT_main
    epyCONTENT_main += ntkHeader1
    epyCONTENT_main += ntkID

    makeLink(headCount, text)


def makeLink(headerNumber, text):
    # convert headerNumber to str, so it can be concatenated with ntkRefText
    headerNumberStr = str(headerNumber)

    ntkRefText = "Chapter " + headerNumberStr + ": " + text
    ntkRef = '<a href="#' + text + '">' + ntkRefText + "</a><br>\n"

    links[headerNumber] = ntkRef

    # append 1 to headCount
    global headCount
    headCount += 1


def toc(size=None):
    # make a table of contents
    
    headerValStart = "<h1>"
    headerValEnd = "</h1>"
    
    # make size=none to make it default to the header 1 size, unless specified
    if size is None or size == 1:
        headerValStart = "<h1>"
        headerValEnd = "</h1>"
    else:
        if size == 2:
            headerValStart = "<h2>"
            headerValEnd = "</h2>"
        elif size == 3:
            headerValStart = "<h3>"
            headerValEnd = "</h3>"
        elif size == 4:
            headerValStart = "<h4>"
            headerValStart = "</h4>"
        else:
            # if input not found then set to default
            headerValStart = "<h1>"
            headerValEnd = "</h1>"

    global epyCONTENT_toc
    
    tocTitle = headerValStart + "<b>Table of Contents</b>" + headerValEnd + "\n"

    epyCONTENT_toc += tocTitle

    global headCount
    for header in range(1, headCount):
        linkTitle = links[header]
        linkTitle += "\n"
        epyCONTENT_toc += linkTitle


def text(text, emphasis=None):
    # write text to the main body of the Notaker file
    # text does not insert a <br> at the end of the text
    emphasis = emphasis.lower()
    if emphasis is None:
        # default text when there are no emphasis tags specified
        ntkP = "<p>" + text + "</p>\n"
    else:
        if emphasis == "b":
            # bold text
            ntkP = "<p><b>" + text + "</b></p>\n"
        elif emphasis == "i":
            # italic text
            ntkP = "<p><i>" + text + "</i></p>\n"
        elif emphasis == "u":
            # underline text
            ntkP = "<p><u>" + text + "</u></p>\n"
        else:
            # if input not found then set to default
            ntkP = "<p>" + text + "</p>\n"

    global epyCONTENT_main
    epyCONTENT_main += ntkP


def textL(text, emphasis=None):
    # write text to the main body of the Notaker file
    # textL inserts a <br> at the end of the text

    if emphasis is None:
        # default text when there are no emphasis tags specified
        ntkP = "<p>" + text + "</p><br>\n"
    else:
        if emphasis == "b":
            # bold text
            ntkP = "<p><b>" + text + "</b></p><br>\n"
        elif emphasis == "i":
            # italic text
            ntkP = "<p><i>" + text + "</i></p><br>\n"
        elif emphasis == "u":
            # underline text
            ntkP = "<p><u>" + text + "</u></p><br>\n"
        else:
            # if input not found then set to default
            ntkP = "<p>" + text + "</p><br>\n"

    global epyCONTENT_main
    epyCONTENT_main += ntkP
