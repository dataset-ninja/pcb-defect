**PCB Defect** is a dataset tailored for an object detection task, encompassing 693 images annotated with 2953 labeled objects across six distinct classes: *open_circuit*, *short*, *spurious_copper*, and other nuanced defects such as *missing_hole*, *mouse_bite*, and *spur*. Specifically curated for **Tiny Defect Detection (TDD)**, the dataset is instrumental for advancing quality control measures in the production of printed circuit boards (PCBs), which is a fundamental and crucial aspect of manufacturing processes in the electronics industry. 

PCB defects can be divided into two categories: functional defects and cosmetic defects. Functional defects can seriously affect the performance of PCB, which may lead to the abnormal usage of PCBs. These defects are the most serious defects. Cosmetic defects mainly affect the appearance of PCB, but also damage its performance in the long run due to abnormal heat dissipation and distribution of current. Among the two categories, there are six kinds of defects which frequently appear in the actual industrial scene. Here, we mainly study these six known and common defects which contain missing hole, mouse bite, open circuit, short, spur, and spurious copper.

<img src="https://github.com/dataset-ninja/pcb-defect/assets/123257559/41f4d3ff-ba8b-400e-bef7-472977ba3ae5" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Some defects examples - a: Missing hole, b: Mouse bite, c: Open circuit, d: Short, e: Spur, f: Spurious copper.</span>

In this figure, defect areas are indicated by thicker and red outlines.

PCB Defect dataset contains 693 PCB defective images and corresponding annotation files. For this dataset, the average pixel size of each image is <i>2,777 x 2,138</i>. The PCB defects include 6 classes (missing hole, mouse bite, open circuit, short, spur, and spurious copper). One image contains several defects. 

| Type of Defects   | Number of Images | Number of Defects |
|-------------------|------------------:|-------------------:|
| Missing Hole      | 115              | 497               |
| Mouse Bite        | 115              | 492               |
| Open Circuit      | 116              | 482               |
| Short             | 116              | 491               |
| Spur              | 115              | 488               |
| Spurious Copper   | 116              | 503               |
| **Total**         | **693**          | **2953**           |

With the respect of such small dataset, data augmentation techniques are adopted before data training. The images are then cropped into 600 × 600 sub-images, forming our training set and testing set with 9920 and 2508 images, respectively. Augmented PCB Defect also [available on DatasetNinja]()
