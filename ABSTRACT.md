**PCB Defect** is a dataset tailored for an object detection task, encompassing 1386 images annotated with 2953 labeled objects across six distinct classes: *open_circuit*, *short*, *spurious_copper*, and other nuanced defects such as *missing_hole*, *mouse_bite*, and *spur*. Specifically curated for **Tiny Defect Detection (TDD)**, the dataset is instrumental for advancing quality control measures in the production of printed circuit boards (PCBs), which is a fundamental and crucial aspect of manufacturing processes in the electronics industry. 

To ensure the representativeness of the dataset, authors build a PCB image acquisition system that resembles the practical AOI system used in inspection process.

<img width="544" alt="pcb_defects_preview_1" src="https://github.com/dataset-ninja/pcb-defect/assets/123257559/aff3d4f1-83e0-4a78-b690-2c5c6e124e8b">

<span style="font-size: smaller; font-style: italic;">The PCB image acquisition system consisting of light source, workbench, support, camera and image process unit.</span>

The image of template board is captured by a 16-megapixel HD industrial camera equipped with CMOS sensor, and it can be controlled by computer software or a remote control. In order to adapt to different PCB sizes and avoid edge distortion, an undistorted zoomable industrial lens is also mounted, the focal length can be adjusted between 6-12 mm and the maximum aperture is <i>f1.6</i>. Light source is also a key part of AOI, to avoid specular reflection of the board, possible shadows and minimize the effects of uneven illumination on subsequent steps, two frosted ring LED source equipped with special diffuse matting board are introduced to effectively overcome the adverse effects of illumination. The resolution of original photo is 4608×3456 pixels, which will be adjusted according to the size of each board when make defects.

After getting cropped image, authors make 6 types of defects by photoshop, which is a graphics editor published by Adobe Systems. The defects authors defined are: missing hole, mouse bite, open circuit, short, spur, spurious copper. Each image in the dataset has 3 to 5 defects of the same category in different places. Besides, authors provide bounding box and coordinate information for every defect in every image, which is convenient for other researchers to know where the defect is. On some inspection platforms, PCB can be fixed by mechanical devices to maintain good position. However, on the assembly line, without fixing equipments, the position and the angle of the test PCB in the taken photo may distinguish from each other. Given this circumstance, in addition to the defects images with the same position as the templates, authors also provide images with random orientations to represent the situation where the image is not appropriately placed in practical detection process. The angular difference between each image and the corresponding template image is also given so that the designing and evaluating of registration algorithm could be implemented on these images.

<img width="416" alt="pcb_defect_preview_2" src="https://github.com/dataset-ninja/pcb-defect/assets/123257559/e7e096db-88c1-47e4-ad06-dbe83c5f5b1b">

<span style="font-size: smaller; font-style: italic;"> Samples of the PCB with defects in the dataset, (a) is the defects image with the same position as template, (b) is the image with random orientation.</span>

Moreover, *rotation* split has PCB images with orientations, and rotation ***angles***

| Type of Defects   | Number of Images | Number of Defects |
|-------------------|------------------:|-------------------:|
| Missing Hole      | 115              | 497               |
| Mouse Bite        | 115              | 492               |
| Open Circuit      | 116              | 482               |
| Short             | 116              | 491               |
| Spur              | 115              | 488               |
| Spurious Copper   | 116              | 503               |
| **Total**         | **693**          | **2953**           |

Also, you can check the **Augmented PCB Defect** [available on DatasetNinja](https://datasetninja.com/augmented-pcb-defect) based on this dataset.
