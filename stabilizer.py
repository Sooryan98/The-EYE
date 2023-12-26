import time
import cv2
import numpy as np



class Trajectory:
    def __init__(self, x=0, y=0, a=0):
        self.x = x
        self.y = y
        self.a = a

    def __add__(self, other):
        return Trajectory(self.x + other.x, self.y + other.y, self.a + other.a)

    def __sub__(self, other):
        return Trajectory(self.x - other.x, self.y - other.y, self.a - other.a)

    def __truediv__(self, scalar):
        if isinstance(scalar, Trajectory):
            return Trajectory(self.x / scalar.x, self.y / scalar.y, self.a / scalar.a)
        else:
            return Trajectory(self.x / scalar, self.y / scalar, self.a / scalar)

    def __mul__(self, scalar):
        if isinstance(scalar, Trajectory):
            return Trajectory(self.x * scalar.x, self.y * scalar.y, self.a * scalar.a)
        else:
            return Trajectory(self.x * scalar, self.y * scalar, self.a * scalar)

def gain(page_num):
    HORIZONTAL_BORDER_CROP = 20
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_AUTOFOCUS,1)
  
    start_time = time.time()  # Record the start time
    duration = 10 # Specify the duration in seconds

    ret, frame_prev = cap.read()  # Initialize frame_prev with the first frame
    if not ret:
        return

    frame_prev = cv2.cvtColor(frame_prev, cv2.COLOR_BGR2GRAY)

    height, width = frame_prev.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_path=page_num+'/stabilized_output.avi'
    print(output_path)
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (width, height),False)
    a, x, y = 0, 0, 0
    X, X_, P, P_, K, z = Trajectory(), Trajectory(), Trajectory(), Trajectory(), Trajectory(), Trajectory()
    pstd, cstd = 4e-3, 0.25
    Q, R = Trajectory(pstd, pstd, pstd), Trajectory(cstd, cstd, cstd)

    k = 1
    vert_border = HORIZONTAL_BORDER_CROP * frame_prev.shape[0] / frame_prev.shape[1]
    rigidtransform, last_rigidtransform = None, None

    while time.time() - start_time <= duration:
        ret, image = cap.read()
        if not ret:
            break

        frame_curr = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        prevpts = cv2.goodFeaturesToTrack(frame_prev, 300, 0.01, 10)
        currpts, status, err = cv2.calcOpticalFlowPyrLK(frame_prev, frame_curr, prevpts, None)

        prev_corner = prevpts[status == 1]
        cur_corner = currpts[status == 1]

        rigidtrans = cv2.estimateAffine2D(prev_corner, cur_corner)[0]

        if rigidtrans is None:
            rigidtrans = last_rigidtransform.copy()

        last_rigidtransform = rigidtrans.copy()

        dx, dy, da = rigidtrans[0, 2], rigidtrans[1, 2], np.arctan2(rigidtrans[1, 0], rigidtrans[0, 0])

        x += dx
        y += dy
        a += da

        z = Trajectory(x, y, a)

        if k == 1:
            X, P = Trajectory(0, 0, 0), Trajectory(1, 1, 1)
        else:
            X_, P_ = X, P + Q
            K = P_ / (P_ + R)
            X = X_ + K * (z - X_)
            P = (Trajectory(1, 1, 1) - K) * P_

        diff_x, diff_y, diff_a = X.x - x, X.y - y, X.a - a

        dx += diff_x
        dy += diff_y
        da += diff_a

        rigidtrans[0, 0] = np.cos(da)
        rigidtrans[0, 1] = -np.sin(da)
        rigidtrans[1, 0] = np.sin(da)
        rigidtrans[1, 1] = np.cos(da)

        rigidtrans[0, 2] = dx
        rigidtrans[1, 2] = dy

        warped_frame = cv2.warpAffine(frame_curr, rigidtrans, (640, 480))
        final_frame = warped_frame[int(vert_border):int(warped_frame.shape[0])-int(vert_border), int(HORIZONTAL_BORDER_CROP):int(warped_frame.shape[1])-int(HORIZONTAL_BORDER_CROP)]
        
        final_frame = cv2.resize(final_frame, (image.shape[1], image.shape[0]))
        out.write(final_frame)
        # cv2.imshow("video", image)
        cv2.imshow("stabilized video", final_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_prev = frame_curr.copy()
        k += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()




"""+-------------------+
|   Start Program   |
+-------------------+
          |
          v
  +-----------------+
  |   Initialize    |
  |   Parameters    |
  +-----------------+
          |
          v
  +-----------------+
  |   Open Video    |
  |   Capture       |
  +-----------------+
          |
          v
+---------------------------------+
|   Read First Frame (prev_image) |
+---------------------------------+
          |
          v
+----------------------------------+
|   Convert prev_image to Grayscale|
+----------------------------------+
          |
          v
+-------------------------+
|   Calculate Dense Optical|
|   Flow (initialization)|
+-------------------------+
          |
          v
  +-----------------------+
  |   Create Kalman Filter|
  |   with Observed Motion|
  +-----------------------+
          |
          v
+----------------------------+
|   Main Loop (duration = 4s) |
|   While time within limit  |
+----------------------------+
          |
          v
+----------------------------------+
|   Read Current Frame (frame_curr)|
+----------------------------------+
          |
          v
+-------------------------------+
|   Convert frame_curr to       |
|   Grayscale                  |
+-------------------------------+
          |
          v
+-------------------------------+
|   Calculate Dense Optical     |
|   Flow (between frame_prev    |
|   and frame_curr)             |
+-------------------------------+
          |
          v
+-----------------------------------+
|   Extract x and y motion meshes  |
|   from the dense optical flow    |
+-----------------------------------+
          |
          v
+-----------------------------------+
|   Aggregate Motion Vectors        |
|   (Calculate Average Motion)      |
+-----------------------------------+
          |
          v
+------------------------------------+
|   Update Kalman Filter with        |
|   Observed Motion (measurement)    |
+------------------------------------+
          |
          v
+--------------------------------------+
|   Apply Stabilization Using Kalman  |
|   Filter Prediction                 |
+--------------------------------------+
          |
          v
+-----------------------------------+
|   Write Stabilized Frame to Output |
+-----------------------------------+
          |
          v
+----------------------------------+
|   Display Original and Stabilized|
|   Video Frames                   |
+----------------------------------+
          |
          v
+---------------------------+
|   Check for User Quit (q) |
+---------------------------+
          |
          v
+---------------------------------+
|   Update Loop Variables (k, bar) |
+---------------------------------+
          |
          v
+----------------------------------+
|   End Loop (Go back to Main Loop)|
+----------------------------------+
          |
          v
+----------------------------------+
|   Check for Program Termination   |
+----------------------------------+
          |
          v
+----------------------------+
|   Release Resources (Video)|
+----------------------------+
          |
          v
  +-------------------+
  |   End Program     |
  +-------------------+
"""