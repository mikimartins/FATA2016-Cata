#! /usr/bin/env python
# -*- coding: utf-8 -*-

from os import listdir, system
from os.path import join, isdir
from time import sleep
from re import sub

if __name__ == "__main__":
    DATA_DIR = "./texts"
    HTML_TEMPLATE = "html.html"
    BOOK_NAME = "FAT-Atibaia-2016"
    TOC_TAG = "<!-- !!! TOCTOCTOC !!! -->"
    BODY_TAG = "<!-- !!! BODYBODY !!! -->"
    BIOS_DIRNAME = "pessoas"
    # ["#78d2ce", "#61ccf6", "#5758b2", "#6b3a9e", "#4e78c5"]

    BODY = ""
    TOC = ""
    idx = 0

    for txtDir in [f for f in sorted(listdir(DATA_DIR)) if isdir(join(DATA_DIR, f))]:
        thisDir = join(DATA_DIR, txtDir)
        thisHeading = sub(r"[0-9]+", "", txtDir).title()

        TOC += "            <h3>%s</h3>\n"%thisHeading
        TOC += "            <ul class=\"toc\">\n"

        if BIOS_DIRNAME in thisDir:
            BODY += "        <h1 class=\"chapter\">%s</h1>\n"%thisHeading
            BODY += "        <h2 class=\"chapter\"></h2>\n"
            BODY += "        <div id=\"bio-container\">\n"

        for filename in [f for f in sorted(listdir(thisDir)) if f.endswith(".txt")]:
            fullPath = join(thisDir, filename)
            print "PROCESSING: %s"%fullPath

            cHtml = ""
            cTitle = ""
            cAuthor = ""
            cTitleColor = "color: #78d2ce;"

            # expand the html and add to TOC list
            with open(fullPath) as txt:
                for line in txt.read().splitlines():
                    if cTitle is "":
                        titleAuthor = line.split(":")
                        cTitle = titleAuthor[0].strip()
                        cAuthor = titleAuthor[-1].strip()
                        cAuthor = '' if (cAuthor == cTitle) else cAuthor
                        TOC += "				<li><a href=\"#ch%s\">%s</a></li>\n"%(str(idx), cTitle)
                    elif line.startswith("color:"):
                        cTitleColor = line.strip()
                    elif "images/" in line:
                        if cHtml is "":
                            if BIOS_DIRNAME in thisDir:
                                cHtml += "            <div id=\"ch%s\" class=\"bio-row\">\n"%str(idx)
                                cHtml += "                <div class=\"bio-name\">%s</div>\n"%cTitle
                                cHtml += "                <div class=\"bio-img\">\n"
                                cHtml += "                    <img src=%s />\n"%line.strip()
                                cHtml += "                </div>\n"
                                cHtml += "                <div class=\"bio-txt\">\n"
                            else:
                                cHtml += "        <div id=\"ch%s\" class=\"projcover\">\n"%str(idx)
                                cHtml += "            <img src=%s />\n"%line.strip()
                                cHtml += "            <h2><span style=\"%s\">%s<br /><span id=\"author\">%s</span></span></h2>\n"%(cTitleColor,cTitle, cAuthor)
                                cHtml += "        </div>\n"
                                cHtml += "        <h1 class=\"chapter\">%s</h1>\n"%cTitle
                                cHtml += "        <h2 class=\"chapter\">%s</h2>\n"%cAuthor
                        # hack to get images on TOC
                        elif " ::TOC:: " in line:
                            srcTitle = line.split(" ::TOC:: ")
                            imgSrc = srcTitle[0].strip()
                            imgTitle = srcTitle[1].strip()
                            idx += 1
                            TOC += "				<li><a href=\"#ch%s\">%s</a></li>\n"%(str(idx), imgTitle)
                            cHtml += "        <div id=\"ch%s\" class=\"projcover\">\n"%str(idx)
                            cHtml += "            <img src=%s />\n"%imgSrc
                            cHtml += "        </div>\n"
                        else:
                            cHtml += "        <div class=\"projcover\">\n"
                            cHtml += "            <img src=%s />\n"%line
                            cHtml += "        </div>\n"
                    else:
                        if BIOS_DIRNAME in thisDir:
                            cHtml += "                    %s\n"%line
                        else:
                            cHtml += "        %s\n"%line
                txt.close()

            if BIOS_DIRNAME in thisDir:
                cHtml += "                </div>\n"
                cHtml += "            </div>\n"

            if cHtml is not "":
                BODY += cHtml
            idx += 1

        # close TOC and bios
        TOC += "            </ul>\n"
        if BIOS_DIRNAME in thisDir:
            BODY += "        </div>\n"

    # write output file
    with open(BOOK_NAME+".html", 'w') as out, open(HTML_TEMPLATE) as temp:
        for line in temp.readlines():
            if TOC_TAG in line:
                line = TOC
            if BODY_TAG in line:
                line = BODY
            out.write(line)
        out.close()
        temp.close()

    # make pdf
    system("prince -s style.css %s.html -o %s.pdf"%(BOOK_NAME,BOOK_NAME))
    system("pdf2ps %s.pdf %s.ps"%(BOOK_NAME,BOOK_NAME))
    system("rm -rf %s.pdf"%(BOOK_NAME))
    system("ps2pdf %s.ps %s.pdf"%(BOOK_NAME,BOOK_NAME))
    system("rm -rf %s.ps"%(BOOK_NAME))
