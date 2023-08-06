from .basic_crop import FaceCropper


def crop_image(img, resolution, landmark_predictor_path, if_mirror_padding=False):
    # img is pil or path
    face_cropper = FaceCropper(r, landmark_predictor_path, esolution, check_resolution=False, mirror_padding=if_mirror_padding, upper_limit_of_black_region_ratio=1.)
    cropped_img = face_cropper.crop_face(img)
    return cropped_imgs

def crop_image_from_path(img_path, resolution, landmark_predictor_path, if_mirror_padding=False):
    face_cropper = FaceCropper(landmark_predictor_path, resolution, check_resolution=False, mirror_padding=if_mirror_padding, upper_limit_of_black_region_ratio=1.)
    cropped_img = face_cropper.crop_face_from_path(img)
    return cropped_img