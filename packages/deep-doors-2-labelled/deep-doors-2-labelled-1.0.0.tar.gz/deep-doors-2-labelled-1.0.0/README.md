# DeepDoors2 Labeled

[![pypi](https://img.shields.io/pypi/v/deep-doors-2-labelled.svg)](https://pypi.org/project/deep-doors-2-labelled/)

To download the new version of DeepDoors2, click [here](https://drive.google.com/file/d/1wSmFUHF9aSJkomwFdOmepMevBvkRpf3D/view?usp=sharing).

This repository contains the necessary code to manage the relabeled version of the [DeepDoors2](https://github.com/gasparramoa/DeepDoors2) dataset. The new dataset version we provide is built to perform object detection over 2D and 3D doors data. Each examples is composed by an 480x640 RGB image, the depth data, and the bounding boxes coordinates with their label. Each doors can assume 3 different statuses: open, semi-open, and closed. The dataset provided in this repo is managed using the [generic-dataset](https://github.com/micheleantonazzi/generic-dataset) package.