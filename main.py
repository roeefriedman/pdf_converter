import os
import copy
import sys
from pypdf import PdfWriter, PdfReader
import argparse


def handle_args(args):
    error = False

    if not os.path.isdir(args.path):
        print(f'Directory not found: {args.path}')
        error = True
    if args.path[-1] != '/':
        args.path += '/'

    if not os.path.isfile(args.path + args.file):
        print(f'File not found: {args.path + args.file}')
        error = True

    if error:
        sys.exit(1)


def optimize_file(file):
    # Sometimes reading and writing will compress the file
    print('Optimizing')
    reader = PdfReader(file)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.add_metadata(reader.metadata)

    with open(file+'_compressed.pdf', "wb") as fp:
        writer.write(fp)


def crop_file(path, filename, direction='V', skip=0, optimize=False):
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

    if optimize:
        optimize_file(path+filename+'_final.pdf')


parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', help='File path', default='./')
parser.add_argument('-f', '--file', help='File name', required=True)
parser.add_argument('-d', '--direction', help='Direction of cropping (v|h)', choices=['v', 'h'], default='v')
parser.add_argument('-s', '--skip_page', help='number of first pages to skip (default = 0)', default=0, type=int)
parser.add_argument('-o', '--optimize', help='Attempt to optimize file size (default = False)', default=False,
                    action='store_true')
cl_args = parser.parse_args()
handle_args(cl_args)

crop_file(cl_args.path, cl_args.file, cl_args.direction.lower(), int(cl_args.skip_page), cl_args.optimize)
