'''
Author: Dai Yalun
Date: 2022-05-18 17:00
'''

#!/usr/bin/env python
import shutil
import os
import argparse
from function import adaptive_instance_normalization
import net
from pathlib import Path
from PIL import Image
import random
import torch
import torch.nn as nn
import torchvision.transforms
from torchvision.utils import save_image
from tqdm import tqdm
from label_xml_tool import update_filename
from label_csv_tool import csv_item_search, csv_stylized_item_add

parser = argparse.ArgumentParser(description='This script applies the AdaIN style transfer method to arbitrary datasets.')
parser.add_argument('--content-dir', type=str,
                    help='Directory path to a batch of content images')
parser.add_argument('--style-dir', type=str,
                    help='Directory path to a batch of style images')
parser.add_argument('--output-dir', type=str, default='output',
                    help='Directory to save the output images')
parser.add_argument('--num-styles', type=int, default=1, help='Number of styles to \
                        create for each image (default: 1)')
parser.add_argument('--alpha', type=float, default=1.0,
                    help='The weight that controls the degree of \
                          stylization. Should be between 0 and 1')
parser.add_argument('--extensions', nargs='+', type=str, default=['png', 'jpeg', 'jpg'], help='List of image extensions to scan style and content directory for (case sensitive), default: png, jpeg, jpg')

# Advanced options
parser.add_argument('--content-size', type=int, default=0,
                    help='New (minimum) size for the content image, \
                    keeping the original size if set to 0')
parser.add_argument('--style-size', type=int, default=512,
                    help='New (minimum) size for the style image, \
                    keeping the original size if set to 0')
parser.add_argument('--crop', type=int, default=0,
                    help='If set to anything else than 0, center crop of this size will be applied to the content image \
                    after resizing in order to create a squared image (default: 0)')

## xml label options
# parser.add_argument('--src-label-path', type=str, default='',
#                     help='path of source xml')
# parser.add_argument('--out-label-path', type=str, default='',
#                     help='path of dst xml')

## csv label option
# parser.add_argument('--src-csv-path', type=str, default='',
#                     help='path of source csv')
# parser.add_argument('--out-csv-path', type=str, default='',
#                     help='path of dst csv')

# random.seed(131213)

def input_transform(size, crop):
    transform_list = []
    if size != 0:
        transform_list.append(torchvision.transforms.Resize(size))
    if crop != 0:
        transform_list.append(torchvision.transforms.CenterCrop(crop))
    transform_list.append(torchvision.transforms.ToTensor())
    transform = torchvision.transforms.Compose(transform_list)
    return transform

def style_transfer(vgg, decoder, content, style, alpha=1.0):
    assert (0.0 <= alpha <= 1.0)
    content_f = vgg(content)
    style_f = vgg(style)
    feat = adaptive_instance_normalization(content_f, style_f)
    feat = feat * alpha + content_f * (1 - alpha)
    return decoder(feat)

def main():
    args = parser.parse_args()

    # set content and style directories
    content_dir = Path(args.content_dir)
    style_dir = Path(args.style_dir)
    style_dir = style_dir.resolve()
    output_dir = Path(args.output_dir)
    output_dir = output_dir.resolve()
    assert style_dir.is_dir(), 'Style directory not found'

    # set xml label directories
    # if args.src_label_path:
    #     src_label_path = Path(args.src_label_path)
    #     src_label_path = src_label_path.resolve()
    #     assert src_label_path.is_dir()
    #     if args.out_label_path:
    #         out_label_path = Path(args.out_label_path)
    #         out_label_path = out_label_path.resolve()
    #         assert out_label_path.is_dir()
    #     else:
    #         out_label_path = src_label_path

    # collect content files
    extensions = args.extensions
    assert len(extensions) > 0, 'No file extensions specified'
    content_dir = Path(content_dir)
    content_dir = content_dir.resolve()
    assert content_dir.is_dir(), 'Content directory not found'
    dataset = []
    for ext in extensions:
        dataset += list(content_dir.rglob('*.' + ext))

    assert len(dataset) > 0, 'No images with specified extensions found in content directory' + content_dir
    content_paths = sorted(dataset)
    print('Found %d content images in %s' % (len(content_paths), content_dir))

    # collect style files
    styles = []
    for ext in extensions:
        styles += list(style_dir.rglob('*.' + ext))

    assert len(styles) > 0, 'No images with specified extensions found in style directory' + style_dir
    styles = sorted(styles)
    print('Found %d style images in %s' % (len(styles), style_dir))

    decoder = net.decoder
    vgg = net.vgg

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    decoder.eval()
    vgg.eval()

    decoder.load_state_dict(torch.load('models/decoder.pth'))
    vgg.load_state_dict(torch.load('models/vgg_normalised.pth'))
    vgg = nn.Sequential(*list(vgg.children())[:31])

    vgg.to(device)
    decoder.to(device)

    content_tf = input_transform(args.content_size, args.crop)
    style_tf = input_transform(args.style_size, 0)


    # disable decompression bomb errors
    Image.MAX_IMAGE_PIXELS = None
    skipped_imgs = []

    # actual style transfer as in AdaIN
    with tqdm(total=len(content_paths)) as pbar:
        for content_path in content_paths:
            try:
                content_img = Image.open(content_path).convert('RGB')
                for style_path in random.sample(styles, args.num_styles):
                    style_img = Image.open(style_path).convert('RGB')

                    content = content_tf(content_img)
                    style = style_tf(style_img)
                    style = style.to(device).unsqueeze(0)
                    content = content.to(device).unsqueeze(0)
                    with torch.no_grad():
                        output = style_transfer(vgg, decoder, content, style,
                                                args.alpha)
                    output = output.cpu()

                    rel_path = content_path.relative_to(content_dir)
                    out_dir = output_dir.joinpath(rel_path.parent)

                    # create directory structure if it does not exist
                    if not out_dir.is_dir():
                        out_dir.mkdir(parents=True)

                    content_name    = content_path.stem
                    style_name      = style_path.stem
                    out_filename    = content_name + '-stylized-' + style_name + content_path.suffix
                    output_name     = out_dir.joinpath(out_filename)

                    # ************************************************* #
                    #                  label generation                 #
                    # ************************************************* #

                    ## xml label generation
                    # src_label_path      = 'F:\graduation_prj\shapedataset-detection\multi-shape-dataset-test\Annotations'
                    # out_label_path      = 'F:\graduation_prj\shapedataset-detection\multi-shape-dataset-test\stylized_Annotations'

                    # if src_label_path:
                    #     src_label_filename  = content_name + '.xml'
                    #     src_label_file      = os.path.join(src_label_path, src_label_filename)
                    #     out_label_filename  = content_name + '-stylized-' + style_name + '.xml'
                    #     out_label_file      = os.path.join(out_label_path, out_label_filename)
                    #     shutil.copyfile(src_label_file, out_label_file)
                    #     update_filename(out_label_file, out_filename, output_name)

                    ## csv label generation
                    src_csv_path = 'F:\graduation_prj\shapedataset-detection\multi-shape-dataset-test\csv_Annotations\csv_labels.csv'
                    out_csv_path = 'F:\graduation_prj\shapedataset-detection\multi-shape-dataset-test\csv_Annotations\csv_labels_style.csv'
                    stylized_imfor = csv_item_search(src_csv_path, content_name + content_path.suffix)
                    csv_stylized_item_add(out_filename, stylized_imfor, out_csv_path)

                    # ************************************************* #

                    save_image(output, output_name, padding=0) #default image padding is 2.
                    style_img.close()
                content_img.close()
            except OSError as e:
                print('Skipping stylization of %s due to an error' %(content_path))
                skipped_imgs.append(content_path)
                continue
            except RuntimeError as e:
                print('Skipping stylization of %s due to an error' %(content_path))
                skipped_imgs.append(content_path)
                continue
            finally:
                pbar.update(1)

    if(len(skipped_imgs) > 0):
        with open(output_dir.joinpath('skipped_imgs.txt'), 'w') as f:
            for item in skipped_imgs:
                f.write("%s\n" % item)

if __name__ == '__main__':
    main()
