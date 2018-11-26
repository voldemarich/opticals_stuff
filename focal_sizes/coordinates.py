from math import pi, sin, cos

camera = {}

camera["x"] = 32000.0
camera["y"] = 20300.0
camera["yaw"] = 3*pi/2

def angle_to_coords(camera_x, camera_y, distance_z, angle, yaw):
    distance_vector = abs(distance_z/(sin(angle)))
    print "ANGLE"
    print angle
    offset_angle = (-1*angle)+yaw
    print offset_angle, distance_vector, distance_vector*cos(offset_angle), distance_vector*sin(offset_angle)
    x = distance_vector*cos(offset_angle)+camera_x
    y = distance_vector*sin(offset_angle)+camera_y
    return x,y

