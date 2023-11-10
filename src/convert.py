import supervisely as sly
import os, glob
from dataset_tools.convert import unpack_if_archive
import src.settings as s
from urllib.parse import unquote, urlparse
from supervisely.io.fs import get_file_name, file_exists, get_file_name_with_ext
import xml.etree.ElementTree as ET
import shutil

from tqdm import tqdm

def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:        
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path
    
def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count
    
def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    dataset_path = "PCB_DATASET"
    batch_size = 50
    ds_name = "ds"
    images_folder = "images"
    anns_folder = "Annotations"
    images_ext = ".jpg"
    bboxes_ext = ".xml"


    def create_ann(image_path):
        labels = []

        ann_path = image_path.replace(images_folder, anns_folder).replace(images_ext, bboxes_ext)

        if file_exists(ann_path):
            tree = ET.parse(ann_path)
            root = tree.getroot()

            img_wight = int(root.find(".//width").text)
            img_height = int(root.find(".//height").text)

            ann_objects = root.findall(".//object")
            for curr_object in ann_objects:
                obj_class_name = curr_object[0].text
                obj_class = name_to_class[obj_class_name]
                left = int(curr_object[4][0].text)
                top = int(curr_object[4][1].text)
                right = int(curr_object[4][2].text)
                bottom = int(curr_object[4][3].text)

                rect = sly.Rectangle(left=left, top=top, right=right, bottom=bottom)
                label = sly.Label(rect, obj_class)
                labels.append(label)

        else:
            image_np = sly.imaging.image.read(image_path)[:, :, 0]
            img_height = image_np.shape[0]
            img_wight = image_np.shape[1]

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)


    missing_hole = sly.ObjClass("missing_hole", sly.Rectangle)
    mouse_bite = sly.ObjClass("mouse_bite", sly.Rectangle)
    open_circuit = sly.ObjClass("open_circuit", sly.Rectangle)
    short = sly.ObjClass("short", sly.Rectangle)
    spur = sly.ObjClass("spur", sly.Rectangle)
    spurious_copper = sly.ObjClass("spurious_copper", sly.Rectangle)

    name_to_class = {
        "missing_hole": missing_hole,
        "mouse_bite": mouse_bite,
        "open_circuit": open_circuit,
        "short": short,
        "spur": spur,
        "spurious_copper": spurious_copper,
    }

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=list(name_to_class.values()))
    api.project.update_meta(project.id, meta.to_json())

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    images_pathes = glob.glob(dataset_path + "/images/*/*.jpg")

    progress = sly.Progress("Create dataset {}".format(ds_name), len(images_pathes))

    for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
        img_names_batch = [get_file_name_with_ext(im_path) for im_path in img_pathes_batch]

        img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns = [create_ann(image_path) for image_path in img_pathes_batch]
        api.annotation.upload_anns(img_ids, anns)

        progress.iters_done_report(len(img_names_batch))

    return project
