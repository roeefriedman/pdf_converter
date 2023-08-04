import os
import shutil
import copy
from pypdf import PdfWriter, PdfReader

PATH = 'C:\\Users\\roefri01\\Downloads\\ariel\\oz2\\'
FILE = 'oz.pdf'


def split_file(filename):
    pdf_file = PdfReader(open(filename, 'rb'))

    for i in range(len(pdf_file.pages)):
        print(i)
        output_pdf = PdfWriter()
        output_pdf.add_page(pdf_file.pages[i])
        with open(PATH+'output_{}.pdf'.format(str(i).zfill(3)), 'wb') as output_file:
            output_pdf.write(output_file)


def duplicate_pages(path):
    for filename in os.listdir(path):
        if 'output_' not in filename:
            continue
        print(f'{path} {filename}')
        shutil.copy2(path+filename, path+filename+'_part1.pdf')
        shutil.move(path+filename, path+filename+'_part2.pdf')


def crop_pages():
    pass


def merge_pages(path):
    output_pdf = PdfWriter()
    files = os.listdir(path)
    files.sort()
    for filename in files:
        print(f'Merging {filename}')
        if 'output_' not in filename:
            continue
        # output_pdf.add_page(PdfReader(open(path+filename, 'rb')).pages[0])
        with open(path+filename, 'rb') as f:
            page = PdfReader(f).pages[0]
            if 'part1' in filename:
                print(f'{page.mediabox.top} {page.mediabox.bottom} {page.mediabox.left} {page.mediabox.right}')
                page.mediabox.bottom = page.mediabox.top / 2
                print(f'{page.mediabox.top} {page.mediabox.bottom} {page.mediabox.left} {page.mediabox.right}')
            else:
                print(f'{page.mediabox.top} {page.mediabox.bottom} {page.mediabox.left} {page.mediabox.right}')
                page.mediabox.top = page.mediabox.top / 2
                print(f'{page.mediabox.top} {page.mediabox.bottom} {page.mediabox.left} {page.mediabox.right}')
            # page = copy.copy(page)
            output_pdf.add_page(page)
        os.remove(path+filename)

    with open(PATH+FILE+'_final.pdf', 'wb') as output_file:
        output_pdf.write(output_file)


print('Start')
split_file(PATH+FILE)
duplicate_pages(PATH)
merge_pages(PATH)
