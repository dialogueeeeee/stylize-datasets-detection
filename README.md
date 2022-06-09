# stylize-datasets-detection
- A script that applies the AdaIN style transfer method to VOC format object detection datasets.
- 本项目是使用 AdaIN 对 VOC 格式的目标检测数据集进行样式迁移的脚本，可以同时生成风格迁移后的图像和对应的标签文件。

## 说明
- 本项目在 [stylize-datasets](https://github.com/bethgelab/stylize-datasets) 基础上进行改进，在原项目的基础上**新增了标签文件的生成**；
- 由于风格迁移后的图像中物体的形状和位置信息基本不改变，所以重新生成的标签文件中的 `object` 信息不发生变化，仅在 `filename` 和 `path` 中改变新图像生成的名称和位置。

## Usage
使用说明。

