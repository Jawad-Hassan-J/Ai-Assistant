import cv2
from ultralytics import YOLO

MODEL_PATH = "yolov10m.pt"
CAM_INDEX = 0
IMGSZ = 320
# IMGSZ = 680
CONF = 0.35
WIDTH = 640
HEIGHT = 480

def main():
    model = YOLO(MODEL_PATH)

    # نفتح الكاميرا
    cap = cv2.VideoCapture(CAM_INDEX)

    # في حال مافتحت
    if not cap.isOpened():
        print("error")
        return
    
    # العرض و الارتفاع
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    while True:
        
        """
        # ok: بولين في حال قرا الفريم
        # feame: الفريم نفسه
        """
        ok, frame = cap.read()

        if not ok:
            break

        """
        الفريم نفسه

        """
        results = model(frame, imgsz=IMGSZ, conf=CONF, stream=True, verbose=False)

        for r in results:
            boxes = r.boxes

            if boxes is None:
                continue

            names = r.names

        num_boxes = len(boxes.xyxy)

        for i in range(num_boxes):
            box = boxes.xyxy[i]
            score = boxes.conf[i]
            cls_id = boxes.cls[i]

            x1, y1, x2, y2 = map(int, box.tolist())
            confidence = float(score.item())
            class_index = int(cls_id.item())
            class_name = names[class_index]

            label_text = f"{class_name} {confidence:.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame,label_text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255, 255, 255), 1,cv2.LINE_AA)

            cv2.imshow("YOLOv10", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    cap.release()
    cv2.destroyAllWindows()
    print("End")

if __name__ == "__main__":
    main()
