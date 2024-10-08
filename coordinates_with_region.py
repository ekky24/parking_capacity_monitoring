# importing the module 
import cv2
import config
import numpy as np
from shapely.geometry import Polygon
from shapely.geometry.point import Point
from datetime import datetime
  
def click_event(event, x, y, flags, params): 
  
    # checking for left mouse clicks 
    if event == cv2.EVENT_LBUTTONDOWN: 
  
        # displaying the coordinates 
        # on the Shell 
        print(x, ' ', y) 
  
        # displaying the coordinates 
        # on the image window 
        font = cv2.FONT_HERSHEY_SIMPLEX 
        cv2.putText(frame, str(x) + ',' +
                    str(y), (x,y), font, 
                    1, (255, 0, 0), 2) 
        cv2.imshow('image', frame) 
  
    # checking for right mouse clicks      
    if event==cv2.EVENT_RBUTTONDOWN: 
  
        # displaying the coordinates 
        # on the Shell 
        print(x, ' ', y) 
  
        # displaying the coordinates 
        # on the image window 
        font = cv2.FONT_HERSHEY_SIMPLEX 
        b = frame[y, x, 0] 
        g = frame[y, x, 1] 
        r = frame[y, x, 2] 
        cv2.putText(frame, str(b) + ',' +
                    str(g) + ',' + str(r), 
                    (x,y), font, 1, 
                    (255, 255, 0), 2) 
        cv2.imshow('image', frame)

# driver function 
if __name__=="__main__": 
  
    # reading the image 
    source = "rtsp://admin:WGNVQB@182.0.21.189:554/ch2/main"
    area = 'stb'

    counting_region = config.LOCATION_CONF[area]['region']

    cv2.namedWindow("image", cv2.WINDOW_NORMAL) 
    frame_w, frame_h = 1280,720

    VideoCapture = cv2.VideoCapture(source)
    while VideoCapture.isOpened():
        sucess, frame = VideoCapture.read()
        if not sucess:
            break
        
        frame = cv2.resize(frame, (frame_w, frame_h))

        cv2.rectangle(frame, (55, 682), (427, 712), (255, 255, 255), -1)
        cv2.putText(frame, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), (56, 709), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)

        # Draw regions (Polygons/Rectangles)
        for region in counting_region:
            region_label = str(region["counts"])
            region_color = region["region_color"]
            region_text_color = region["text_color"]

            polygon_coords = np.array(region["polygon"].exterior.coords, dtype=np.int32)
            centroid_x, centroid_y = int(region["polygon"].centroid.x), int(region["polygon"].centroid.y)

            text_size, _ =cv2.getTextSize(
                region_label, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.7, thickness=2
            )
            text_x = centroid_x - text_size[0] // 2
            text_y = centroid_y + text_size[1] // 2
            
            cv2.polylines(frame, [polygon_coords], isClosed=True, color=region_color, thickness=2)

        # displaying the image 
        cv2.imshow('image', frame) 
        cv2.setMouseCallback('image', click_event) 
    
        # wait for a key to be pressed to exit 
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
  
    # close the window 
    cv2.destroyAllWindows() 