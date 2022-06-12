# stylize-datasets-detection
- A script that applies the AdaIN style transfer method to VOC format object detection datasets.
- 本项目是使用 AdaIN 对 VOC 格式的目标检测数据集进行样式迁移的脚本，可以同时生成风格迁移后的图像和对应的标签文件。

## Introduction
- 本项目在 [stylize-datasets](https://github.com/bethgelab/stylize-datasets) 基础上进行改进，在原项目的基础上**新增了标签文件的生成**；
- 由于风格迁移后的图像中物体的形状和位置信息基本不改变，所以重新生成的标签文件中的 `object` 信息不发生变化，仅在 `filename` 和 `path` 中改变新图像生成的名称和位置。

## Usage
stylize a dataset, run python `stylize.py`. Arguments like below:

- `--content-dir <CONTENT>` the top-level directory of the content image dataset (mandatory)
- `--style-dir <STLYE>` the top-level directory of the style images (mandatory)
- `--output-dir <OUTPUT>` the directory where the stylized dataset will be stored (optional, default: output/)
- `--num-styles <N>` number of stylizations to create for each content image (optional, default: 1)
- `--alpha <A>` Weight that controls the strength of stylization, should be between 0 and 1 (optional, default: 1)
- `--extensions <EX0> <EX1> ...` list of image extensions to scan style and content directory for (optional, default: png, jpeg, jpg). Note: this is case sensitive, --extensions jpg will not scan for files ending on .JPG. Image types must be compatible with PIL's Image.open() (Documentation)
- `--content-size <N>` Minimum size for content images, resulting in scaling of the shorter side of the content image to N (optional, default: 0). Set this to 0 to keep the original image dimensions.
- `--style-size <N>` Minimum size for style images, resulting in scaling of the shorter side of the style image to N (optional, default: 512). Set this to 0 to keep the original image dimensions (for large style images, this will result in high (GPU) memory consumption).
- `--crop <N>` Size for the center crop applied to the content image in order to create a squared image (optional, default 0). Setting this to 0 will disable the cropping.
- `--src-label-path <CONTENT LABEL>` the top-level directory of the xml label for content image dataset 
- `--out-label-path <STLYE LABEL>` the top-level directory of the xml label for style image dataset 
