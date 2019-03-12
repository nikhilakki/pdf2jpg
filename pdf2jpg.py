__author__ = "Nikhil Akki"
__version__ = "1.0"

'''
pdf-to-jpg-converter.py converts PDF to JPG images

example usage: python pdf-to-jpg-converter.py -i input-pdf/ -o output-jpgs/

'''


import asyncio
import os
from pdf2image import convert_from_path
import logging
import time
import argparse


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info('logged init')


def list_pdfs(path='resume-data/data'):
    files = os.listdir(path)
    pdfs = [i for i in files if i.split('.')[-1] == 'pdf']
    return pdfs


def pdf_convert(file_path, dpi=500):
    pages = convert_from_path(file_path, dpi)
    return pages

def convert_resume_to_img(file_path, save_dir='resume_images', dpi=500):
    pages = pdf_convert(file_path, dpi)
    logging.info('No. of pages: {}'.format(len(pages)))
    document_name = file_path.split('/')[-1].split('.')[0]
    document_name = document_name.replace('+', '_')
    page_len = len(pages)
    for i, page in enumerate(pages):
        current_page = i + 1
        logging.info('Saving page: {}'.format(current_page))
        page.save('{}/{}_page_{}of{}.jpg'.format(save_dir, document_name, current_page, page_len))
        logging.info('Page {} saved'.format(current_page))
    logging.info('{} resume pages converted to jpg'.format(document_name))


async def convert(path='resume-data/data', save_dir='resume_images', dpi=500):
    try:
        files = list_pdfs(path)
        if len(files) > 0:
            for file in files:
                file_path = os.path.join(path, file)
                convert_resume_to_img(file_path, save_dir=save_dir, dpi=dpi)
                await asyncio.sleep(0.01)
    except Exception as e:
        logging.warning('Error: {}'.format(e))

async def main(path, save_dir, dpi=500):
    await asyncio.wait([
        convert(path=path, save_dir=save_dir, dpi=dpi)
    ])


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='PDF to JPG Converter')
    parser.add_argument('-i', '--input', required=True,
                        help="Input dir containing PDF files")
    parser.add_argument('-o', '--output', required=True,
                        help="Output dir where images will be exported")
    ap = vars(parser.parse_args())
    resume_dir = ap['input']
    save_dir = ap['output']
    loop = asyncio.get_event_loop()
    t0 = time.time()
    loop.run_until_complete(main(resume_dir, save_dir))
    t1 = time.time()
    logging.warning('Took: {} seconds to complete'.format(t1-t0))
