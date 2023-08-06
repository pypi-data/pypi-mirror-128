# Image preprocessing tools

##  crop face and rotate

### requiements
- PIL
- opencv
- dlib

### usage

- `simple_crop.py`

```
python simple_crop.py input_dir output_dir resolution [--mirror_padding]
```

If you set `resolution` to `-1`, you can skip resizing process. If you add `--mirror_padding` option, images are mirror padded.

To run the program, you will need `shape_predictor_68_face_landmarks.dat` 
, which you can get from https://github.com/davisking/dlib-models 

## resize oversize images

### requiements
- PIL

### usage
- `resize_square.py`

```
python resize_square.py image_dir image_out_dir resolution
```

## split by size

### requiements
- PIL

### usage
- `size_split.py`

```
python size_split.py input_dir output_dir split_size
```

## Remove top and side
Remove L pixels on the top and L / 2 pixels on the left and right of the image.
### requiements
- opencv
### usage
- `delete_region_other_than_below.py`
```
python delete_region_other_than_below.py --image_dir --L --output_dir [--workers]
```
