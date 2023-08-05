import os
import copy
import sys
from pypdf import PdfWriter, PdfReader
import argparse


def crop_file(path, filename, direction='V', skip=0):
    # open input file, PdfReader
    input_pdf_file = PdfReader(open(path+filename, 'rb'))
    # create PdfWriter
    output_pdf = PdfWriter()
    # loop over pages

    for i in range(len(input_pdf_file.pages)):
        print(f'Processing page {i} of {len(input_pdf_file.pages)}')
        # add bottom/left page
        page = input_pdf_file.pages[i]
        if i < skip:
            output_pdf.add_page(page)
            continue
        mb = copy.copy(page.mediabox)  # Save a copy of the original page.mediabox properties
        # print(f'{page.mediabox.top} {page.mediabox.bottom} {page.mediabox.left} {page.mediabox.right}')
        if direction == 'v':
            page.mediabox.bottom = page.mediabox.top / 2
        else:
            page.mediabox.left = page.mediabox.right / 2
        output_pdf.add_page(page)
        page.mediabox = copy.copy(mb)  # Restore the mediabox properties

        # add top/right
        if direction == 'v':
            page.mediabox.top = page.mediabox.top / 2
        else:
            page.mediabox.right = page.mediabox.right / 2
        output_pdf.add_page(page)

    # Write output file
    with open(path + filename + '_final.pdf', 'wb') as output_file:
        output_pdf.write(output_file)

    # Sometimes reading and writing will compress the file
    # reader = PdfReader(PATH+FILE+'_final.pdf')
    # writer = PdfWriter()
    #
    # for page in reader.pages:
    #     writer.add_page(page)
    #
    # writer.add_metadata(reader.metadata)
    #
    # with open(PATH+FILE+'_compressed.pdf', "wb") as fp:
    #     writer.write(fp)


def handle_args(args):
    error = False
    if args.path is None:
        args.path = './'
    if not os.path.isdir(args.path):
        print(f'Directory not found: {args.path}')
        error = True
    if args.path[-1] != '/':
        args.path += '/'

    if args.file is None:
        print('File not found: None')
        error = True
    if not os.path.isfile(args.path + args.file):
        print(f'File not found: {args.path + args.file}')
        error = True

    if args.skip_page is None:
        args.skip_page = '0'
    if not args.skip_page.isnumeric():
        print(f'skip_page should be a number: {args.skip_page}')
        error = True

    if args.direction is None:
        args.direction = 'v'
    if args.direction.lower() != 'v' and args.direction.lower() != 'h':
        print(f'direction can be v or h: {args.direction}')
        error = True

    if error:
        sys.exit(1)


parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', help='File path')
parser.add_argument('-f', '--file', help='File name')
parser.add_argument('-d', '--direction', help='Direction of cropping (v|h)')
parser.add_argument('-s', '--skip_page', help='number of first pages to skip (default = 0)')
cl_args = parser.parse_args()
handle_args(cl_args)

crop_file(cl_args.path, cl_args.file, cl_args.direction.lower(), int(cl_args.skip_page))
