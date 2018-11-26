from math import atan, pi


def angle_tan(pixelsize, matrix_mm, matrix_pixel, focal): # this is tan of the viewangle/2, may be used in each axis
    matrixsize = (float(pixelsize) / matrix_pixel) * matrix_mm
    return (matrixsize * 0.5) / focal


def distance_z(realsize_mm_y, pixelsize_y, matrix_mm_y, matrix_pixel_y, focal):
    return (realsize_mm_y*0.5)/angle_tan(pixelsize_y, matrix_mm_y, matrix_pixel_y, focal)


def full_collection(x_begin,
                    x_end,
                    matrix_mm_x,
                    matrix_pixel_x,
                    realsize_mm_y,
                    pixelsize_y,
                    matrix_mm_y,
                    matrix_pixel_y,
                    focal): # returns collection in mm (0, start of object, fin of object, total)
    col = {}
    pixelsize_x = x_end-x_begin
    pixelsize_after = matrix_pixel_x-x_end
    pixelsize_before = matrix_pixel_x-pixelsize_after-pixelsize_x
    dst_z = distance_z(realsize_mm_y, pixelsize_y, matrix_mm_y, matrix_pixel_y, focal)
    x_angle = atan(angle_tan(pixelsize_x, matrix_mm_x, matrix_pixel_x, focal))*2
    before_angle = atan(angle_tan(pixelsize_before, matrix_mm_x, matrix_pixel_x, focal))*2
    after_angle = atan(angle_tan(pixelsize_after, matrix_mm_x, matrix_pixel_x, focal))*2
    print x_angle, before_angle, after_angle
    # if pixelsize_after > matrix_pixel_x/2.0:
    #     after_angle = after_angle+pi/2
    # if pixelsize_before > matrix_pixel_x/2.0:
    #     before_angle = after_angle+pi/2
    # if pixelsize_x > matrix_pixel_x/2.0:
    #     x_angle = after_angle+pi/2

    offset_angle = ((pi)-(before_angle+after_angle+x_angle))/2.0
    print before_angle+after_angle+x_angle+offset_angle
    col["x_angle"] = (offset_angle+after_angle+x_angle)
    col["distance_z"] = dst_z
    return col
