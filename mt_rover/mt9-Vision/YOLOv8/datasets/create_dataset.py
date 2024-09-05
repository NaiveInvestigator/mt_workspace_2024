from roboflow import Roboflow

rf = Roboflow(api_key="3G0qNCUt7yzhJpyFixjm")
project = rf.workspace("bracu-mongoltori").project("bottle-detection-zjxba")
dataset = project.version(1).download("yolov8")