from ultralytics import YOLO

model = YOLO('yolov8n.pt') 
results = model.train(data='Bottle-Detection-1\data.yaml', epochs=5, imgsz=640)
print(results)