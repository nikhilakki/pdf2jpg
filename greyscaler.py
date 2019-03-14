import logging
import asyncio
from pathlib import os
from PIL import Image
import time
import argparse


logging.basicConfig(
    #  filename='greyscaler.log',
     level=logging.INFO,
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )

def greyscaler(image_path, img, save_dir):
    file_name = os.path.join(image_path, img)
    image = Image.open(file_name).convert('L')
    image.save('{}'.format(os.path.join(save_dir, img)))
    logging.info('{} converted to grey scale and saved to disk'.format(img))


async def call(image_path, save_dir):
    imgs = os.listdir(image_path)
    imgs = [i for i in imgs if i.split('.')[-1]=='jpg']
    try:
        for img in imgs:
            greyscaler(image_path, img, save_dir)
            await asyncio.sleep(0.01)
    except Exception as e:
        logging.warning('Found error: {}'.format(e))


async def main(image_path, save_dir):

    await asyncio.wait([
        call(image_path, save_dir)
    ])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Image to Greyscale Converter')
    parser.add_argument('-i', '--input', required=True,
                        help="Input dir containing PDF files")
    parser.add_argument('-o', '--output', required=True,
                        help="Output dir where images will be exported")
    ap = vars(parser.parse_args())
    input_dir = ap['input']
    output_dir = ap['output']

    logging.info('Getting event loop')
    loop = asyncio.get_event_loop()
    logging.info('Starting jobs in event loop')
    t0 = time.time()
    loop.run_until_complete(main(input_dir, output_dir))
    logging.info('Event loop closed')
    t1 = time.time()
    logging.warning('Took {} secs to complete the job'.format(t1-t0))

