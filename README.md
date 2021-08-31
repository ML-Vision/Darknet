# Darknet

1. Jetson AGX xavier OS 설치

2. Jetson AGX xavier에 darknet 설치

3. Train은 colab과 미니PC 두 곳에서 가능합니다.

UI 사용에 관하여

- UI 사용시 Data를 선택하는 Root 경로는 Image_to_Train 폴더입니다.

- 모델이 저장되는 경로는 darknet/models/(모델 이름) 입니다.

- colab에서 모델 Train시 작업이 끝나면 weights가 /backup폴더에 저장이 됩니다.
미니PC의 darknet/models/해당 폴더(모델 이름) 에 /obj.data , obj.names, yolov4-obj.cfg, weights 총 4개의 파일을 저장하면 됩니다.

- Camera 로 Detect시 실행 전에 바슬러 카메라 가이드를 보고 해당 작업을 먼저 해주시길 바랍니다.


(https://drive.google.com/drive/folders/1KPYbZX4Y_55dBhmQdVUeMxamsfxopIZm?usp=sharing
해당 파일 참조)
