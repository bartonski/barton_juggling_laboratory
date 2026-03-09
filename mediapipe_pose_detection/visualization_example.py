# Mediapipe hand detecton
# TODO: Move into module
# TODO: Get centroid of hand (or perhaps just track base of middle finger?)
# See https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker#pose_landmarker_model for diagram of landmarks.

# 0 - nose --
# 1 - left eye (inner)
# 2 - left eye
# 3 - left eye (outer)
# 4 - right eye (inner)
# 5 - right eye
# 6 - right eye (outer)
# 7 - left ear
# 8 - right ear
# 9 - mouth (left)
# 10 - mouth (right)
# 11 - left shoulder
# 12 - right shoulder
# 13 - left elbow --
# 14 - right elbow --
# 15 - left wrist --
# 16 - right wrist --
# 17 - left pinky --
# 18 - right pinky --
# 19 - left index --
# 20 - right index --
# 21 - left thumb --
# 22 - right thumb --
# 23 - left hip
# 24 - right hip
# 25 - left knee
# 26 - right knee
# 27 - left ankle
# 28 - right ankle
# 29 - left heel
# 30 - right heel
# 31 - left foot index
# 32 - right foot index

# We can use the x coordinate for 'nose' as the center line of the pattern.
# The landmarks we care about for juggling are left and right elbow,
# wrist, pinky, index and thumb. From the samples that I've looked at,
# the fingers aren't very accurate, but elbow and wrist are.

import cv2
import sys

# ---
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np

juggling_landmarks = {
    "nose"        : 0,
    "left_elbow"  : 13,
    "right_elbow" : 14,
    "left_wrist"  : 15,
    "right_wrist" : 16,
    "left_pinky"  : 17,
    "right_pinky" : 18,
    "left_index"  : 19,
    "right_index" : 20,
    "left_thumb"  : 21,
    "right_thumb" : 22
}

def draw_landmarks_on_image(rgb_image, detection_result):
  pose_landmarks_list = detection_result.pose_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected poses to visualize.
  for idx in range(len(pose_landmarks_list)):
    pose_landmarks = pose_landmarks_list[idx]

    # Draw the pose landmarks.
    pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    pose_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
    ])
    solutions.drawing_utils.draw_landmarks(
      annotated_image,
      pose_landmarks_proto,
      solutions.pose.POSE_CONNECTIONS,
      solutions.drawing_styles.get_default_pose_landmarks_style())
  return annotated_image
# ---

filename = str(sys.argv[-1])

cap = cv2.VideoCapture(filename)

cv2.namedWindow("Juggling", cv2.WINDOW_NORMAL)

ret, frame = cap.read()

while ret:
    # STEP 2: Create an PoseLandmarker object.
    base_options = python.BaseOptions(model_asset_path='pose_landmarker_heavy.task')
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        output_segmentation_masks=True)
    detector = vision.PoseLandmarker.create_from_options(options)

    # STEP 3: Load the input image.
    cv_mat = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv_mat)

    # STEP 4: Detect pose landmarks from the input image.
    detection_result = detector.detect(image)

    # STEP 5: Process the detection result. In this case, visualize it.
    annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)

    cv2.imshow("Juggling", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

    key = cv2.waitKey(1)
    if key == 27:
        break

    ret, frame = cap.read()

cap.release()
cv2.destroyAllWindows()

