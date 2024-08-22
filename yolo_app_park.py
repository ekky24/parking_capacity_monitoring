import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
previous_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(previous_dir)

import argparse
import pytz
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

import os
import shutil
import subprocess
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

current_region = None

def cleaning(VideoCapture, cv2):
    VideoCapture.release()
    cv2.destroyAllWindows()

def connect_rtsp(source):
    # Video Setup
    VideoCapture = cv2.VideoCapture(source)
    VideoCapture.set(cv2.CAP_PROP_FPS, config.FRAME_RATE)
    
    return VideoCapture

def run(
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
    save_interval = 10
    rtsp_server_url = f"rtsp://localhost:8554/parking_monitoring/{area}"
    ffmpeg_command = [
        'ffmpeg',
        '-y',  # Overwrite output files
        '-f', 'rawvideo',  # Input format
        '-vcodec', 'rawvideo',
        '-pix_fmt', 'bgr24',  # Pixel format
        '-s', '640x360',  # Frame size
        '-re',  # Frame rate
        '-i', '-',  # Input from stdin
        '-c:v', 'libx264',  # Video codec
        '-pix_fmt', 'yuv420p',  # Output pixel format
        '-preset', 'veryfast',
        '-f', 'rtsp',  # Output format
        rtsp_server_url  # Output URL
    ]
    timezone = pytz.timezone(config.TIMEZONE)

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
    
    frame_w, frame_h = 1280, 720
    codec = "mp4v"
    curr_ts = datetime.now(timezone)
    str_curr_date = curr_ts.strftime("%Y%m%d")
    str_curr_ts = curr_ts.strftime("%Y%m%d_%H%M%S")

    VideoCapture = connect_rtsp(source)

    # Iterate and analyze over video frames
    prev_time = 0
    save_start_time = time.time()
    process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)
    frame_count = 0
    
    while True:
        save_curr_time = time.time()

        sucess, frame = VideoCapture.read()
        if not sucess:
            print('INFO: Video capture failed')

            # reconnecting and cleaning
            cleaning(VideoCapture, cv2)
            VideoCapture = connect_rtsp(source)

            continue
        
        # skipping frames
        if frame_count < config.SKIP_FRAMES:
            frame_count += 1
            continue
        frame_count = 0

        frame = cv2.resize(frame, (frame_w, frame_h))
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time

        cv2.rectangle(frame, (55, 682), (427, 712), (255, 255, 255), -1)
        cv2.putText(frame, datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S"), (56, 709), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)

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
                
        if save_curr_time - save_start_time >= save_interval:
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

        # Send to RTSP Stream 
        frame_resize = cv2.resize(frame, (640, 360))

        try:
            process.stdin.write(frame_resize.tobytes())
        except:
            # process.stdin.close()
            # process.wait()
            # print('err send')

            # # reconnecting
            # process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)
            # process.stdin.write(frame_resize.tobytes())
            # continue

            break

        if view_img:
            cv2.imshow("Crowd Counter POC", frame)
        
        for region in counting_region: # Reinitialize counter 
            region["counts"] = 0

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        
    cleaning(VideoCapture, cv2)
    process.stdin.close()
    process.wait()

def parse_opt():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", type=str, default="yolov8n.pt", help="initial weights path")
    parser.add_argument("--device", default="", help="cuda device, i.e. 0 or 0,1,2,3 or cpu")
    parser.add_argument("--source", type=str, required=True, help="video file path")
    parser.add_argument("--view-img", action="store_true", help="show results")
    parser.add_argument("--save-img", action="store_true", help="save results")
    parser.add_argument("--exist-ok", action="store_true", help="existing project/name ok, do not increment")
    parser.add_argument("--classes", nargs="+", type=int, help="filter by class: --classes 0, or --classes 0 2 3")
    parser.add_argument("--line-thickness", type=int, default=2, help="bounding box thickness")
    parser.add_argument("--region-thickness", type=int, default=4, help="Region thickness")
    parser.add_argument("--area", type=str, default="", help="CCTV location")

    return parser.parse_args()


def main(opt):
    """Main function."""
    run(**vars(opt))


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
