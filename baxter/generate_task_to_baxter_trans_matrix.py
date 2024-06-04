import cv2
import numpy as np

##################
# This file generates a transformation matrix from task/board coordinates (12x12 board) to baxter arm endpoint coordinates (X,Y)
##################

# baxter right arm X,Y board positions
tl = [0.796970518711915, -0.36106476655606434]
tr = [0.7197446451729097, -0.813104494522384]
bl = [0.338301030018582, -0.2909917783616702]
br = [0.2755985931901246, -0.7408127684193746]

dst_pts = np.float32([tl, tr, bl, br]) # physical coords
src_pts = np.float32([[0.0, 0.0], [12.0, 0.0], [0.0, 12.0], [12.0, 12.0]]) # task coords

# get tranformation matrix
H = cv2.getPerspectiveTransform(src_pts, dst_pts)

# print and test with task coord
print(H)
input1 = np.float32(np.array([[[1, 5]]]))
coords = cv2.perspectiveTransform(input1, H)[0]
print(coords)
