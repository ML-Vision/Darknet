# Darknet

## Linux

기본 설정

1. Jetson AGX xavier OS 설치

2. Jetson AGX xavier에 darknet 설치 (해당 파일은 Jetson Xavier AGX 기준으로 작성되어 있어 GPU가 달라진다면 설정 부분을 변경해줘야 합니다.)

3. Train은 colab과 미니PC 두 곳에서 가능합니다.

UI 사용

- UI 사용시 Data를 선택하는 Root 경로는 Image_to_Train 폴더입니다.

- 모델이 저장되는 경로는 darknet/models/(모델 이름) 입니다.

- colab에서 모델 Train시 작업이 끝나면 weights가 /backup폴더에 저장이 됩니다.
미니PC의 darknet/models/해당 폴더(모델 이름) 에 /obj.data , obj.names, yolov4-obj.cfg, weights 총 4개의 파일을 저장하면 됩니다.

- Camera 로 Detect시 실행 전에 바슬러 카메라 가이드를 보고 해당 작업을 먼저 해주시길 바랍니다.


## WINDOW (2021.09.14)

윈도우는 기본적으로 darknet을 빌드시 Visual studio가 필요합니다.


### **필요 프로그램**


Visual studio 설치
https://visualstudio.microsoft.com/ko/vs/older-downloads/

CUDA 설치 
https://developer.nvidia.com/cuda-toolkit-archive

CUDNN 설치 (CUDA 버전과 호완되는 걸로 설치)
https://developer.nvidia.com/rdp/cudnn-archive

opencv 설치 
https://opencv.org/releases/

### **참고 영상**

1. https://www.youtube.com/watch?v=FE2GBeKuqpc&t=389s (darknet)
2. https://www.youtube.com/watch?v=tjXkW0-4gME (opencv)

2번 영상에서 OpenCV를 CUDA를 이용해 BUILD하는 부분이 있는데 이부분은 하셔도 되고 안하셔도 됩니다.
(하는게 속도는 조금 더 빠르지 않을까 생각합니다.)


### **UI 사용**

- Window에선 darknet 빌드시 ./darknet/bulid/darknet/x64/ 경로에 실행파일과 yolo_cpp_dll.dll 파일이 생성되기 때문에 작업공간을 해당 경로로 잡았습니다.

- cmd 창에서 python main.py로 UI를 실행하거나 다른 IDE로 실행해도 됩니다.

- UI 사용시 Data를 선택하는 Root 경로는 Image_to_Train 폴더입니다.

- 모델이 저장되는 경로는 darknet/models/(모델 이름) 입니다.

- colab에서 모델 Train시 작업이 끝나면 weights가 /backup폴더에 저장이 됩니다.
- darknet/models/해당 폴더(모델 이름) 에 /obj.data , obj.names, yolov4-obj.cfg, weights 총 4개의 파일을 저장하면 됩니다.

- Camera 로 Detect시 실행 전에 바슬러 카메라 가이드를 보고 해당 작업을 먼저 해주시길 바랍니다.

- Detection할 Image를 선택하는 경로는 test_image/(파일명 or 폴더명) 입니다.

- Detection된 Image가 저장되는 경로는 Image_Predictions/(모델 이름)/ 입니다.

- Camera_Detection에 Web_cam detection을 추가했습니다.

- 실시간으로 촬영한 사진은 CAM_Detections/(모델 이름)/으로 저장되도록 설정해놨습니다.

### 용량이 큰 파일 다운로드 

- yolov4.weights --> https://drive.google.com/file/d/1MZgorvsiHlaojaAHBqM9XMuiIwQi0dKe/view?usp=sharing
(테스트 용 학습된 가중치)
- yolov4.conv.137 -->https://drive.google.com/uc?id=1JKF-bdIklxOOVy-2Cr5qdvjgGpmGfcbp
(학습용 가중치. 경로는 (자신의 경로)\darknet\build\darknet\x64에 저장하면 됩니다.)
