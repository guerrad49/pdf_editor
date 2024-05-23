#!/usr/bin/env python3

import os
import sys
import argparse
from PyPDF2 import PdfReader, PdfMerger, PdfWriter


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument('file', help='Main PDF to work on')
    p.add_argument('-s', '--split', action='store_true',
                   help='Get each page as individual PDF.')
    p.add_argument('-m', '--merge', nargs='*',
                   help='Merge additional PDFs to main PDF.')
    p.add_argument('-o', '--reorder',
                   help='Reorder pages according to comma-separated list.')
    p.add_argument('-r', '--remove',
                   help='Remove page(s) according to comma-separated list.')

    args = p.parse_args()
    
    return args


def split_pdf(base, parentFile):
    reader = PdfReader(parentFile)
    if reader.is_encrypted:
        sys.exit('ERROR - File {} is encrypted.\n'.format(parentFile))

    for i,page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        outName = '{}_page{:02d}.pdf'.format(parentFile[:-4], i+1)
        outName = os.path.join(base, outName)
        with open(outName, 'wb') as f:
            writer.write(f)


def merge_pdfs(base, in_list):
    merger = PdfMerger()

    for file in in_list:
        reader = PdfReader(file)
        if reader.is_encrypted:
            sys.exit('ERROR - File {} is encrypted.\n'.format(file))
        merger.append(reader)

    outName = os.path.join(base, 'merged_file.pdf')
    with open(outName, 'wb') as f:
        merger.write(f)


def reorder_pages(base, parentFile, inOrder):
    reader = PdfReader(parentFile)
    if reader.is_encrypted:
        sys.exit('ERROR - File {} is encrypted.\n'.format(parentFile))

    inOrder = [int(i)-1 for i in inOrder.split(',')]
    
    if len(inOrder) == 2:
        order = list(range(len(reader.pages)))
        order[inOrder[0]],order[inOrder[1]]=order[inOrder[1]],order[inOrder[0]]
    elif len(inOrder) > 2 and len(inOrder) < len(reader.pages):
        order = list(range(min(inOrder)))
        order += inOrder
        order += list(range(max(inOrder)+1,len(reader.pages)))
    elif len(inOrder) == len(reader.pages):
        order = inOrder

    writer = PdfWriter()
    for i in order:
        writer.add_page(reader.pages[i])

    outName = '{}_reordered.pdf'.format(parentFile[:-4])
    outName = os.path.join(base, outName)
    with open(outName, 'wb') as f:
        writer.write(f)


def remove_pages(base, parentFile, inPages):
    reader = PdfReader(parentFile)
    if reader.is_encrypted:
        sys.exit('ERROR - File {} is encrypted.\n'.format(parentFile))

    pgs_to_rm = [int(i)-1 for i in inPages.split(',')]

    writer = PdfWriter()
    for i in range(len(reader.pages)):
        if i not in pgs_to_rm:
            writer.add_page(reader.pages[i])

    outName = '{}_fixed.pdf'.format(parentFile[:-4])
    outName = os.path.join(base, outName)
    with open(outName, 'wb') as f:
        writer.write(f)

    
#=============================================================

if __name__ == '__main__':
    
    args = parse_args()
    basename = os.path.dirname(args.file)

    if args.split:
        split_pdf(basename, args.file)
    elif args.merge:
        mergeList = [args.file] + args.merge
        merge_pdfs(basename, mergeList)
    elif args.reorder:
        reorder_pages(basename, args.file, args.reorder)
    elif args.remove:
        remove_pages(basename, args.file, args.remove)
 
