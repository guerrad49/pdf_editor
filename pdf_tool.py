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


def split_pdf(base, parent_file):
    reader = PdfReader(parent_file)
    if reader.is_encrypted:
        sys.exit('ERROR - File {} is encrypted.\n'.format(parent_file))

    for i,page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        out_name = '{}_page{:02d}.pdf'.format(parent_file[:-4], i+1)
        out_name = os.path.join(base, out_name)
        with open(out_name, 'wb') as f:
            writer.write(f)


def merge_pdfs(base, in_list):
    merger = PdfMerger()

    for file in in_list:
        reader = PdfReader(file)
        if reader.is_encrypted:
            sys.exit('ERROR - File {} is encrypted.\n'.format(file))
        merger.append(reader)

    out_name = os.path.join(base, 'merged_file.pdf')
    with open(out_name, 'wb') as f:
        merger.write(f)


def reorder_pages(base, parent_file, in_order):
    reader = PdfReader(parent_file)
    if reader.is_encrypted:
        sys.exit('ERROR - File {} is encrypted.\n'.format(parent_file))

    in_order = [int(i)-1 for i in in_order.split(',')]
    
    if len(in_order) == 2:
        order = list(range(len(reader.pages)))
        order[in_order[0]],order[in_order[1]]=order[in_order[1]],order[in_order[0]]
    elif len(in_order) > 2 and len(in_order) < len(reader.pages):
        order = list(range(min(in_order)))
        order += in_order
        order += list(range(max(in_order)+1,len(reader.pages)))
    elif len(in_order) == len(reader.pages):
        order = in_order

    writer = PdfWriter()
    for i in order:
        writer.add_page(reader.pages[i])

    out_name = '{}_reordered.pdf'.format(parent_file[:-4])
    out_name = os.path.join(base, out_name)
    with open(out_name, 'wb') as f:
        writer.write(f)


def remove_pages(base, parent_file, in_pages):
    reader = PdfReader(parent_file)
    if reader.is_encrypted:
        sys.exit('ERROR - File {} is encrypted.\n'.format(parent_file))

    pgs_to_rm = [int(i)-1 for i in in_pages.split(',')]

    writer = PdfWriter()
    for i in range(len(reader.pages)):
        if i not in pgs_to_rm:
            writer.add_page(reader.pages[i])

    out_name = '{}_fixed.pdf'.format(parent_file[:-4])
    out_name = os.path.join(base, out_name)
    with open(out_name, 'wb') as f:
        writer.write(f)

    
#=============================================================

if __name__ == '__main__':
    
    args = parse_args()
    basename = os.path.dirname(args.file)

    if args.split:
        split_pdf(basename, args.file)
    elif args.merge:
        merge_list = [args.file] + args.merge
        merge_pdfs(basename, merge_list)
    elif args.reorder:
        reorder_pages(basename, args.file, args.reorder)
    elif args.remove:
        remove_pages(basename, args.file, args.remove)
 
