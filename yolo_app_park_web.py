import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
previous_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(previous_dir)

import argparse
import time
from collections import defaultdict
from pathlib import Path
from datetime import datetime
import torch

import cv2
import numpy as np
from shapely.geometry import Polygon
from shapely.geometry.point import Point

from ultralytics import YOLO
from ultralytics.utils.files import increment_path
from ultralytics.utils.plotting import Annotator, colors
import sqlalchemy as db
import pandas as pd

from data.db_credentials import DB_CONFIG
import dist.config as config
# import config

import os
import shutil
from flask import Flask, Response
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

current_region = None
app = Flask(__name__)

def cleaning(VideoCapture, cv2, save_dir, str_curr_ts):
    VideoCapture.release()
    cv2.destroyAllWindows()

    # clearing tmp
    try:
        os.remove(f"{save_dir}/{str_curr_ts}.mp4")
    except FileNotFoundError:
        print(f"File not found.")
    except PermissionError:
        print(f"Permission denied to delete.")
    except Exception as e:
        print(f"Error occurred while trying to delete: {e}")

def connect_rtsp(source, codec, frame_w, frame_h, save_dir, str_curr_ts):
    # Video Setup
    VideoCapture = cv2.VideoCapture(source)
    VideoCapture.set(cv2.CAP_PROP_FPS, config.FRAME_RATE)
    frame_w_0, frame_h_0, fps = (int(VideoCapture.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, 
                                                                cv2.CAP_PROP_FRAME_HEIGHT, 
                                                                cv2.CAP_PROP_FPS
                                       ))

    video_writer = cv2.VideoWriter(f"{save_dir}/{str_curr_ts}.mp4",
                cv2.VideoWriter_fourcc(*codec), 12, (frame_w,frame_h))
    
    return VideoCapture, video_writer

def generate_frames(
        weights="yolov10m.pt",
        source=None,
        device="gpu",
        view_img=False,
        save_img=False,
        exist_ok=False,
        classes=None,
        line_thickness=2,
        region_thickness=2,
        area=None
):
    """
    Run Region counting on a video using YOLOv10 and ByteTrack.

    Supports movable region for real time counting inside specific area.
    Supports multiple regions counting.
    Regions can be Polygons or rectangle in shape

    Args:
        weights (str): Model weights path.
        source (str): Video file path.
        device (str): processing device cpu, 0, 1
        view_img (bool): Show results.
        save_img (bool): Save results.
        exist_ok (bool): Overwrite existing files.
        classes (list): classes to detect and track
        line_thickness (int): Bounding box thickness.
        track_thickness (int): Tracking line thickness
        region_thickness (int): Region thickness.
        max_parking_cap (int) : Maximum parking capacity
    """
    save_interval = 30
    save_start_time = time.time()

    # Check source path
    if source == 'rtsp':
        cctv_host = config.LOCATION_CONF[area]['host']
        cctv_username = config.LOCATION_CONF[area]['username']
        cctv_pass = config.LOCATION_CONF[area]['password']
        cctv_area = config.LOCATION_CONF[area]['area']

        source = f"rtsp://{cctv_username}:{cctv_pass}@{cctv_host}"

        counting_region = config.LOCATION_CONF[area]['region']
    
    else:
        counting_region = [
            {
                "name": "Counting Region",
                "polygon": Polygon([(440, 91), (510, 89), (465, 358), (217, 357)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            }
        ]
        if not Path(source).exists():
            raise FileNotFoundError(f"Source path '{source}' does not exist.")
    
    # Setup Model
    model = YOLO(f"{weights}")
    
    if torch.cuda.is_available():
        print("GPU is available.")
        device = torch.device('cuda')
    else:
        print("GPU is not available, using CPU.")
        device = torch.device('cpu')

    model.to(device)

    # Extract class names
    names = model.model.names
    codec = "mp4v"

    frame_w, frame_h = 1280, 720
    curr_ts = datetime.now()
    str_curr_date = curr_ts.strftime("%Y%m%d")
    str_curr_ts = curr_ts.strftime("%Y%m%d_%H%M%S")

    # save_dir = f'output/parking_monitoring/{cctv_area}/{str_curr_date}'
    save_dir = f'output/parking_monitoring/tmp/{cctv_area}/{str_curr_date}'
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
        os.makedirs(save_dir.replace('/tmp', ''))

    VideoCapture, video_writer = connect_rtsp(source, codec, frame_w, frame_h, save_dir, str_curr_ts)

    # Iterate and analyze over video frames
    prev_time = 0
    
    while True:
        save_curr_time = time.time()

        sucess, frame = VideoCapture.read()
        if not sucess:
            print('INFO: Video capture failed')

            # reconnecting and cleaning
            cleaning(VideoCapture, cv2, save_dir, str_curr_ts)
            VideoCapture, video_writer = connect_rtsp(source, codec, frame_w, frame_h, save_dir, str_curr_ts)

            continue
        
        frame = cv2.resize(frame, (frame_w, frame_h))
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        cv2.putText(frame, f"{fps:.2f} fps", (7, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 0), 1, cv2.LINE_AA)

        # Extract the results
        results = model.track(frame, persist=True, classes=classes)

        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            clss = results[0].boxes.cls.cpu().tolist()
            annotator = Annotator(frame, line_width=line_thickness, example=str(names))

            for box, track_id, cls in zip(boxes, track_ids, clss):
                bbox_center = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2

                # Check if detection inside region
                for region in counting_region:
                    is_inside_region = region["polygon"].contains(Point((bbox_center[0], bbox_center[1])))
                    if is_inside_region:
                        annotator.box_label(box, color=colors(cls,True)) # kotak deteksi yg didalam region
                        region["counts"] += 1
                            

        # Draw regions (Polygons/Rectangles)
        for counter_idx, region in enumerate(counting_region):
            region_label = str(region["counts"])
            region_color = region["region_color"]
            region_text_color = region["text_color"]

            polygon_coords = np.array(region["polygon"].exterior.coords, dtype=np.int32)
            centroid_x, centroid_y = int(region["polygon"].centroid.x), int(region["polygon"].centroid.y)

            text_size, _ =cv2.getTextSize(
                region_label, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.7, thickness=line_thickness
            )
            text_x = centroid_x - text_size[0] // 2
            text_y = centroid_y + text_size[1] // 2
            cv2.rectangle(
                frame,
                (text_x -5, text_y - text_size[1]-5),
                (text_x + text_size[0] + 5, text_y + 5),
                region_color,
                -1
            )
            cv2.putText(
                frame, region_label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, region_text_color, line_thickness
            )
            cv2.polylines(frame, [polygon_coords], isClosed=True, color=region_color, thickness=region_thickness)
        
            # Parking left
            # x, y = region["polygon"].exterior.coords.xy
            parking_left = config.LOCATION_CONF[area]['max_capacity'][counter_idx] - region["counts"]
            # cv2.putText(frame, f"Parking available : {parking_left}", (int(frame_w/2), 20), 
                        # cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 0), 1, cv2.LINE_AA)
                
        # save output and db
        if save_curr_time - save_start_time >= save_interval:
            source_vid_path = f"{save_dir}/{str_curr_ts}.mp4"
            dest_vid_path = f"{save_dir.replace('/tmp', '')}/{str_curr_ts}.mp4"

            updated_ts = datetime.now()
            str_curr_ts = updated_ts.strftime("%Y%m%d_%H%M%S")

            save_start_time = save_curr_time
            video_writer.release()

            # check if file video is corrupt
            if os.path.exists(source_vid_path):
                file_size = os.path.getsize(source_vid_path)
                if file_size > config.FILE_SIZE_THRESHOLD * 1024:
                    # move file to final dir
                    shutil.move(source_vid_path, dest_vid_path)

            if curr_ts.date() != updated_ts.date():
                curr_ts = updated_ts
                str_curr_date = curr_ts.strftime("%Y%m%d")
                save_dir = f'output/parking_monitoring/tmp/{cctv_area}/{str_curr_date}'
                if not os.path.isdir(save_dir):
                    os.makedirs(save_dir)
                    os.makedirs(save_dir.replace('/tmp', ''))

            video_writer = cv2.VideoWriter(f"{save_dir}/{str_curr_ts}.mp4",
                        cv2.VideoWriter_fourcc(*codec), 12, (frame_w,frame_h))

            # save db
            new_data = {
                'current_occupancy': [],
                'max_capacity': [],
                'area': [],
            }

            for i, region in enumerate(counting_region):
                new_data['current_occupancy'].append(region["counts"])
                new_data['max_capacity'].append(config.LOCATION_CONF[area]['max_capacity'][i])
                new_data['area'].append(region["name"])

            new_data_df = pd.DataFrame(new_data)

            engine = db.create_engine(f"mysql+mysqlconnector://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/cctv",echo=False)
            new_data_df.to_sql('parking_monitoring', con=engine, if_exists="append", index=False)
            engine.dispose()

        print(f"FPS : {fps:.2f}")

        if view_img:
            cv2.imshow("Crowd Counter POC", frame)
        
        if save_img:
            video_writer.write(frame)
        
        for region in counting_region: # Reinitialize counter 
            region["counts"] = 0

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        
        frame = cv2.resize(frame, (640, 360))

        encode_param = [int(cv2.IMWRITE_WEBP_QUALITY), 70]
        ret, buffer = cv2.imencode('.webp', frame, encode_param)
        if not ret:
            continue
        frame = buffer.tobytes()
        # Yield the frame in MJPEG format
        yield (b'--frame\r\n'
                   b'Content-Type: image/webp\r\n\r\n' + frame + b'\r\n')

    cleaning(VideoCapture, cv2, save_dir, str_curr_ts)

@app.route('/video_feed')
def video_feed():
    par_cctv_area = os.getenv('CCTV_AREA')
    return Response(generate_frames(
        weights="yolov8l.pt",
        source='rtsp',
        device=0,
        view_img=False,
        save_img=True,
        exist_ok=False,
        classes=2,
        line_thickness=2,
        region_thickness=2,
        area=par_cctv_area
    ),
    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)
