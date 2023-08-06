from .basic_crop import FaceCropper


def crop_image(img, resolution, if_mirror_padding=False):
    # img is pil or path
    face_cropper = FaceCropper(resolution, check_resolution=False, mirror_padding=if_mirror_padding, upper_limit_of_black_region_ratio=1.)
    cropped_img = face_cropper.crop_face(img)
    return cropped_img

def crop_image_from_path(img_path, resolution, if_mirror_padding=False):
    face_cropper = FaceCropper(resolution, check_resolution=False, mirror_padding=if_mirror_padding, upper_limit_of_black_region_ratio=1.)
    cropped_img = face_cropper.crop_face_from_path(img)
    return cropped_img