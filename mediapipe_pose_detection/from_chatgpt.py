import sys
import cv2
import mediapipe as mp

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

min_lx=0
max_lx=0
min_rx=0
max_rx=0
min_ly=0
max_ly=0
min_ry=0
max_ry=0
min_y=0
max_y=0
mean_lx=0
mean_rx=0
mean_ly=0
mean_ry=0

frame1=True
frame_number=1
min_mid=0
max_mid=0


# Open webcam (or replace "0" with a video filename)


filename = str(sys.argv[-1])

cap = cv2.VideoCapture(filename)

# Store hand trajectories
left_hand_path = []
right_hand_path = []

cv2.namedWindow("Hand Trajectories", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Hand Trajectories", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    
    # Process frame
    results = pose.process(image)
    
    # Convert back to BGR
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    h, w, _ = image.shape
    if frame1:
        print( f"height: {h} width: {w}")
    
    if results.pose_landmarks:
        # Draw landmarks
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )
        
        # Extract hand coordinates
        landmarks = results.pose_landmarks.landmark
        
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_INDEX]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_INDEX]
        nose = landmarks[mp_pose.PoseLandmark.NOSE]
        
        # Convert to pixel coordinates
        lx, ly = int(left_wrist.x * w), int(left_wrist.y * h)
        rx, ry = int(right_wrist.x * w), int(right_wrist.y * h)
        mid_x = int(nose.x * w)

        max_lx = max(max_lx, lx)
        max_rx = max(max_rx, rx)
        max_ly = max(max_ly, ly)
        max_ry = max(max_ry, ry)
        max_mid = max(max_mid, mid_x)

        if( ly > max_y or ry > max_y ):
            max_y = max( ly,ry )
            print( f"min_y: {min_y} max_y: {max_y}" )
        if frame1:
            min_lx = max_lx
            min_rx = max_rx
            min_ly = max_ly
            min_ry = max_ry
            min_y = max_y
            min_mid = max_mid

        if( ly < min_y or ry < min_y ):
            min_y = min( ly,ry )
            print( f"frame_number: {frame_number} min_y: {min_y} max_y: {max_y}" )

        min_lx = min(min_lx, lx)
        min_rx = min(min_rx, rx)
        min_ly = min(min_ly, ly)
        min_ry = min(min_ry, ry)
        mean_lx=int( (max_lx + min_lx)/2 )
        mean_rx=int( (max_rx + min_rx)/2 )
        mean_ly=int( (max_ly + min_ly)/2 )
        mean_ry=int( (max_ry + min_ry)/2 )
        min_mid=min(min_mid, mid_x)
        mean_lr_mid= int( (mean_lx+mean_rx)/2 )
 
        # Append to paths
        left_hand_path.append((lx, ly))
        right_hand_path.append((rx, ry))
        
        # Draw trajectories
        trail_length = 15
        start_left=(len(left_hand_path) - trail_length)
        if start_left < 1:
            start_left = 1
        end_left=len(left_hand_path) 

        start_right=(len(right_hand_path) - trail_length)
        if start_right < 1:
            start_right = 1
        end_right=len(right_hand_path) 

        for i in range(start_left, end_left):
            cv2.line(image, left_hand_path[i-1], left_hand_path[i], (0, 255, 0), 2)
        for i in range(start_right, end_right):
            cv2.line(image, right_hand_path[i-1], right_hand_path[i], (0, 0, 255), 2)
        
        #print( f"line: ({max_mid},{0}),({max_mid},{h})" )
        cv2.line(image, (min_lx,0), (min_lx,h), (63,63,63), 2)
        cv2.line(image, (mean_lx,0), (mean_lx,h), (127,127,127), 2)
        cv2.line(image, (max_lx,0), (max_lx,h), (255,255,255), 2)
        cv2.line(image, (min_rx,0), (min_rx,h), (63,63,63), 2)
        cv2.line(image, (mean_rx,0), (mean_rx,h), (127,127,127), 2)
        cv2.line(image, (max_rx,0), (max_rx,h), (255,255,255), 2)
        cv2.line(image, (0,min_ly), (w,min_ly), (0,63,0), 2)
        cv2.line(image, (0,mean_ly), (w,mean_ly), (0,127,0), 2)
        cv2.line(image, (0,max_ly), (w,max_ly), (0,255,0), 2)
        cv2.line(image, (0,min_ry), (w,min_ry), (0,0,63), 2)
        cv2.line(image, (0,mean_ry), (w,mean_ry), (0,0,127), 2)
        cv2.line(image, (0,max_ry), (w,max_ry), (0,0,255), 2)
        cv2.line(image, (min_mid,0), (min_mid,h), (0,0,0), 2)
        cv2.line(image, (max_mid,0), (max_mid,h), (255,255,255), 2)
        cv2.line(image, (mean_lr_mid,0), (mean_lr_mid,h), (0,255,255), 2)
        cv2.line(image, (mean_lx,mean_ly), (lx,ly), (0,255,0), 2)
        cv2.line(image, (mean_rx,mean_ry), (rx,ry), (0,0,255), 2)
    
    cv2.imshow("Hand Trajectories", image)
    frame1=False
    frame_number += 1
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
