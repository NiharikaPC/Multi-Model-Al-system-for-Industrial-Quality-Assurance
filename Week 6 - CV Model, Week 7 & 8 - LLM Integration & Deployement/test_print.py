from ultralytics import YOLO

model = YOLO("best.pt")

results = model("test_images/sample.jpg")

results[0].show()

print(results[0].boxes)

#ctrl+shift+p -> python: select interpreter