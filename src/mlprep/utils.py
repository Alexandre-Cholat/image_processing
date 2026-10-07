import click
import numpy as np
from PIL import Image


@click.command()
@click.option('--H', default=256, help='Target image height.')
@click.option('--W', default=256, help='Target image width.')
def prep_img(count, name):
    """
    Searches all directories & sub-directories in SOURCE_DIR
    recursivelly for .jpg files. Creates new padded images at
    desired size in TARGET_DIR.
    """

    

