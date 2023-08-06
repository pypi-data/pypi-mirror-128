# Copyright (C) 2021, Mindee.

# This program is licensed under the Apache License version 2.
# See LICENSE or go to <https://www.apache.org/licenses/LICENSE-2.0.txt> for full license details.

import os
from typing import Any, Callable, Dict, List, Optional, Tuple

import defusedxml.ElementTree as ET
import numpy as np

from .datasets import VisionDataset

__all__ = ['SVT']


class SVT(VisionDataset):
    """SVT dataset from `"The Street View Text Dataset - UCSD Computer Vision"
    <http://vision.ucsd.edu/~kai/svt/>`_.

    Example::
        >>> from doctr.datasets import SVT
        >>> train_set = SVT(train=True, download=True)
        >>> img, target = train_set[0]

    Args:
        train: whether the subset should be the training one
        sample_transforms: composable transformations that will be applied to each image
        rotated_bbox: whether polygons should be considered as rotated bounding box (instead of straight ones)
        **kwargs: keyword arguments from `VisionDataset`.
    """

    URL = 'http://vision.ucsd.edu/~kai/svt/svt.zip'
    SHA256 = '63b3d55e6b6d1e036e2a844a20c034fe3af3c32e4d914d6e0c4a3cd43df3bebf'

    def __init__(
        self,
        train: bool = True,
        sample_transforms: Optional[Callable[[Any], Any]] = None,
        rotated_bbox: bool = False,
        **kwargs: Any,
    ) -> None:

        super().__init__(self.URL, None, self.SHA256, True, **kwargs)
        self.sample_transforms = sample_transforms
        self.train = train
        self.data: List[Tuple[str, Dict[str, Any]]] = []
        np_dtype = np.float32

        # Load xml data
        tmp_root = os.path.join(self.root, 'svt1')
        xml_tree = ET.parse(os.path.join(tmp_root, 'train.xml')) if self.train else ET.parse(
            os.path.join(tmp_root, 'test.xml'))
        xml_root = xml_tree.getroot()

        for image in xml_root:
            name, _, _, resolution, rectangles = image

            # File existence check
            if not os.path.exists(os.path.join(tmp_root, name.text)):
                raise FileNotFoundError(f"unable to locate {os.path.join(tmp_root, name.text)}")

            if rotated_bbox:
                _boxes = [
                    [float(rect.attrib['x']) + float(rect.attrib['width']) / 2,
                     float(rect.attrib['y']) + float(rect.attrib['height']) / 2,
                     float(rect.attrib['width']), float(rect.attrib['height'])]
                    for rect in rectangles
                ]
            else:
                _boxes = [
                    [float(rect.attrib['x']), float(rect.attrib['y']),
                     float(rect.attrib['x']) + float(rect.attrib['width']),
                     float(rect.attrib['y']) + float(rect.attrib['height'])]
                    for rect in rectangles
                ]
            # Convert them to relative
            w, h = int(resolution.attrib['x']), int(resolution.attrib['y'])
            boxes = np.asarray(_boxes, dtype=np_dtype)
            boxes[:, [0, 2]] /= w
            boxes[:, [1, 3]] /= h

            # Get the labels
            labels = [lab.text for rect in rectangles for lab in rect]

            self.data.append((name.text, dict(boxes=boxes, labels=labels)))

        self.root = tmp_root

    def extra_repr(self) -> str:
        return f"train={self.train}"
