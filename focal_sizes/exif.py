import exifread


def get_tagcloud(path):
    imgfile = open(path, "r")
    tags_col = exifread.process_file(imgfile, stop_tag="EXIF FocalLength")
    imgfile.close()
    return tags_col


def get_focal_len(tagcloud):
    return int(str(tagcloud["EXIF FocalLength"]))


def get_dims(tagcloud):
    return int(str(tagcloud["EXIF ExifImageWidth"])), int(str(tagcloud["EXIF ExifImageLength"]))


def get_matrix_mm(n=None): # FUKKEN HARDCOOOOOOOODE
    return 22.2, 14.7


