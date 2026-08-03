from ultralytics import YOLO

model = YOLO("yolov8m.pt")
model.export(format="onnx", imgsz=640, opset=19)
