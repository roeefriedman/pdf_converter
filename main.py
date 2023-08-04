import os
import shutil
import copy
from pypdf import PdfWriter, PdfReader

PATH = r'C:\Users\roefri01\Downloads\ariel\\'
FILE = 'l.pdf'
DIR = 'H'
SKIP = 1


def crop_file(path, filename):
    # open input file, PdfReader
    input_pdf_file = PdfReader(open(path+filename, 'rb'))
    # create PdfWriter
    output_pdf = PdfWriter()
    # loop over pages

    for i in range(len(input_pdf_file.pages)):
        print(f'Processing page {i} of {len(input_pdf_file.pages)}')
        # add bottom/left page
        page = input_pdf_file.pages[i]
        if i < SKIP:
            output_pdf.add_page(page)
            continue
        mb = copy.copy(page.mediabox)  # Save a copy of the original page.mediabox properties
        # print(f'{page.mediabox.top} {page.mediabox.bottom} {page.mediabox.left} {page.mediabox.right}')
        if DIR == 'V':
            page.mediabox.bottom = page.mediabox.top / 2
        else:
            page.mediabox.left = page.mediabox.right / 2
        output_pdf.add_page(page)
        page.mediabox = copy.copy(mb)  # Restore the mediabox properties

        # add top/right
        if DIR == 'V':
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


crop_file(PATH, FILE)


