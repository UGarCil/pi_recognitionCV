import cv2
import torch
# %matplotlib inline #for interactive mode of plt
from os.path import join as jn
# import pygame
import numpy as np 
from ultralytics import YOLO

# # Load a model
# model = YOLO("yolov8n.yaml")  # build a new model from scratch
# model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

# def main():
#     # Use the model
#     model.train(data="coco128.yaml", epochs=3)  # train the model
#     metrics = model.val()  # evaluate model performance on the validation set
#     results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image
#     success = model.export(format="onnx")  # export the model to ONNX format

# if __name__ == "__main__":
#     main()

#####################load model for visualization ##############################
# model = YOLO("yolov5l.pt")
# model = torch.hub.load('ultralytics/yolov5', 'yolov8s', pretrained=True)
model = torch.hub.load('ultralytics/yolov5', "custom", path="./UGC_models/july2024.pt",force_reload=True)
for k, v in model.named_parameters():
    print(k)

# img = "test3.jpg"
# results = model(img)
# results.print()

############################################
cap = cv2.VideoCapture(1)
WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * 0.2)
HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * 0.2)

while cap.isOpened():
    _,frame = cap.read()
    frame = cv2.resize(frame, (WIDTH,HEIGHT))
    results = model(frame)
    cv2.imshow("live view",np.squeeze(results.render()))
    # boxes = results.xyxy[0]
    # print(len(boxes))

    # for box in boxes:
    #     x1,x2,w,h = box.tolist()

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
######################################

 

