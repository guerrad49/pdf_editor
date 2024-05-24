#!/usr/bin/env python3

import os
import sys
import argparse
from PyPDF2 import PdfReader, PdfMerger, PdfWriter


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument('file', help='Main PDF to work on')

    g = p.add_mutually_exclusive_group()
    g.add_argument('-s', '--split', action='store_true',
                   help='Get each page as individual PDF.')
    g.add_argument('-m', '--merge', nargs='*',
                   help='Merge additional PDFs to main PDF.')
    g.add_argument('-o', '--reorder',
                   help='Reorder pages according to comma-separated list.')
    g.add_argument('-r', '--remove',
                   help='Remove page(s) according to comma-separated list.')

    args = p.parse_args()

    # convert to 0-indexed list of integers
    if args.reorder:
        args.reorder = [int(x)-1 for x in args.reorder.split(',')]
    if args.remove:
        args.remove = [int(x)-1 for x in args.remove.split(',')]
    
    return args


def split(dirPath, fileName):
    """
    Split and save all PDF pages into separate PDF.
    
    Parameters
    ----------
    dirPath: str
        The full directory path of the PDF file
    fileName: str
        The name of the PDF file
    """

    reader = PdfReader(fileName)

    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        outName = '{}_page{:02d}.pdf'.format(fileName[:-4], i+1)
        outPath = os.path.join(dirPath, outName)
        with open(outPath, 'wb') as f:
            writer.write(f)


def merge(dirPath, filesToMerge):
    """
    Merge a list of PDFs into one.

    Parameters
    ----------
    dirPath: str
        The full directory path of the PDF file
    filesToMerge: list
        The list of PDF names to merge
    """
    
    merger = PdfMerger()
    for file in filesToMerge:
        reader = PdfReader(file)
        merger.append(reader)

    outName = os.path.join(dirPath, 'merged_file.pdf')
    with open(outName, 'wb') as f:
        merger.write(f)


def reorder(dirPath, fileName, order):
    """
    Merge a list of PDFs into one.

    Parameters
    ----------
    dirPath: str
        The full directory path of the PDF file
    fileName: str
        The name of the PDF file
    order: list
        The list of page numbers to reorder
    """

    reader = PdfReader(fileName)
    pdfLen = len(reader.pages)
    
    # start with pages to remain in place
    reordered = [p for p in range(pdfLen) if p not in order]

    # insert other pages with specified order
    indices = sorted(order)
    for i, p in zip(indices, order):
        reordered.insert(i, p)

    writer = PdfWriter()
    for p in reordered:
        writer.add_page(reader.pages[p])

    outName = '{}_reordered.pdf'.format(fileName[:-4])
    outPath = os.path.join(dirPath, outName)
    with open(outPath, 'wb') as f:
        writer.write(f)


def remove(dirPath, fileName, pgsToRemove):
    """
    Remove given files from PDF.

    Parameters
    ----------
    dirPath: str
        The full directory path of the PDF file
    fileName: str
        The name of the PDF file
    pgsToRemove: list
        The list of pages to remove
    """

    reader = PdfReader(fileName)
    pdfLen = len(reader.pages)
    
    pgsToKeep = [p for p in range(pdfLen) if p not in pgsToRemove]

    writer = PdfWriter()
    for p in pgsToKeep:
        writer.add_page(reader.pages[p])

    outName = '{}_fixed.pdf'.format(fileName[:-4])
    outPath = os.path.join(dirPath, outName)
    with open(outPath, 'wb') as f:
        writer.write(f)


def check_encryption(fileList):
    """Checks encryption and exits program if so."""
    
    for f in fileList:
        reader = PdfReader(f)
        if reader.is_encrypted:
            msg = 'ERROR - File {} is encrypted.\n'.format(f)
            sys.exit(msg)

    
#=============================================================

if __name__ == '__main__':
    args = parse_args()
    basename = os.path.dirname(args.file)

    if args.split:
        check_encryption([args.file])
        split(basename, args.file)
    elif args.merge:
        mergeList = [args.file] + args.merge
        check_encryption(mergeList)
        merge(basename, mergeList)
    elif args.reorder:
        check_encryption([args.file])
        reorder(basename, args.file, args.reorder)
    elif args.remove:
        check_encryption([args.file])
        remove(basename, args.file, args.remove)
 
