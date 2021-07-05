# Fproject

# 1. 데이터 수집
Selenium을 사용해 stayc 멤버의 이미지 데이터 수집
- https://github.com/SeleniumHQ/selenium
- Google-image-crawling 사용하려 했으나 구글 정책 바뀜에 따라 막힘

< 문제점 & 해결방안 >
- 데이터 양의 부족
    - 신인 그룹이라 데이터 양이 적었다.
    - 그룹 변경 (stays -> black pink)
- 무대 사진 외의 기사 사진 등도 섞여있어 무대 영상을 예측 시 예측률이 떨어짐
    - 예측할 영상과 가장 유사한 데이터를 사용해야 좋은 결과를 낼 수 있겠다! 
    - 무대 직캠 영상을 지정 프레임마다 캡쳐해 데이터로 사용


# 2.  데이터 라벨링
Lableimg-master 사용해 라벨링
- https://github.com/tzutalin/labelImg

< 데이터 라벨링 기준 >
- 얼굴이 확실하게 구분 가능한 경우에만 라벨링
- 동선/옷차림 등의 조건을 고려하지 않고도 구분 가능한 경우
- 머리카락으로 얼굴이 가려져있거나 뒤돌아 있는 경우에는 라벨링 제외
- 라벨링 사이즈: 헤어스타일이 나오게 라벨링(두상 - 어깨 선 정도까지)
- 낮은 화질(360p)의 데이터도 구비
- 총 2160장    


=> 화질이 낮은 데이터를 포함해 학습시켜 성능이 낮을 수도 있다는 멘토님 의견에 이후 1080p 데이터만 따로 추려서 학습 (총 1316장)    


# 3-1. 좌표 추출 / 정리?
영상 detect 시 --save-txt flag를 사용하여 예측 좌표 csv 파일로 저장    
저장한 csv파일을 각 멤버별로 분리    

    - 기존 yolov5 모델은 frame별로 예측한 좌표를 개별 txt 파일로 저장하는 형식
        -> detect.py file 내부 함수를 수정해 영상 전체 txt 파일을 묶어 하나의 csv 파일로 저장되게 함
    # - 예측하지 못한 frame은 좌표가 출력되지 않음
    #    -> 영상의 모든 frame별 좌표를 받아 crop 해야 하기 때문에 0으로 채운 dataframe을 만들고 둘을 합침
    - null값 처리 / smoothing
        - 이동평균 알고리즘
    

# 3-2. 영상 크롭
Opencv 사용
멤버별 csv 파일에서 frame별 좌표값을 받아 각 frame을 crop 후 VideoWriter의 writer 메소드를 사용해 영상으로 저장

- 일부 프레임이 빠지고 저장되는 경우 발생 
    - > 원인 : 좌표에서 목표 범위 만큼 더하고 뺄 경우 기존 영상의 범위를 나가는 경우가 발생하여 writer 메소드 실행시 불포함하고 영상으로 저장
    - > 해결 : 좌표 + 목표 영상크기가 범위 밖일 경우 영상 범위에서 목표크기로 추출할 수 있는 가장 끝값으로 출력하는 알고리즘 추가
   

# 4. 모델
### YOLOv5 모델 사용

1. 특징
- 기존 연구들과 다르게 '속도' 중심. 빠르다!
    - 기존 연구들이 '정확도'를 중요하게 생각했으나, 실시간 반영 문제가 발생하여 이를 극복하고자 함
    - You Only Look Once
    - Multi-task 문제를 하나의 회귀 문제로 재정의
        - 이미지 전체에 대해서 '하나의 신경망'이 '한번의 계산'으로 'bounding box', 'class probabilty' 예측
            - bounding box: object detection 대상에 빨간 박스
            - class probability: 분류 및 예측하고자하는 대상의 종류와 확률
- 기존 방식들보다 background error가 적다.
    - 기존 'Sliding Window', 'Region proposal' 방식과 다르게, 훈련과 테스트 단계에서 이미지 전체를 인식.
    - 기존 방식의 단점: Background Error(아무 물체가 없는 배경에 반점, 노이즈 등이 있으면 물체로 인식)
- 물체의 일반적인 부분을 학습하기에 다른 모델에 비해 보지 못한 새로운 이미지에 대해 더 robust함
- 단점
    - 다른 모델들에 비해 정확도가 떨어진다.
        
        
[img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FlqVvp%2FbtqKv79n5Pr%2FlJJ0EoK0sb8kVrLShiMo7k%2Fimg.png)



2. YOLOv5 세부모델의 종류
[img](https://github.com/ultralytics/yolov5/releases/download/v1.0/model_comparison.png)



| Model                                                        | size (pixels) | mAPval 0.5:0.95 | mAPtest 0.5:0.95 | mAPval 0.5 | Speed V100 (ms) |      | params (M) | FLOPS 640 (B) |
| ------------------------------------------------------------ | ------------- | --------------- | ---------------- | ---------- | --------------- | ---- | ---------- | ------------- |
| [YOLOv5s6](https://github.com/ultralytics/yolov5/releases)   | 1280          | 43.3            | 43.3             | 61.9       | **4.3**         |      | 12.7       | 17.4          |
| [YOLOv5m6](https://github.com/ultralytics/yolov5/releases)   | 1280          | 50.5            | 50.5             | 68.7       | 8.4             |      | 35.9       | 52.4          |
| [YOLOv5l6](https://github.com/ultralytics/yolov5/releases)   | 1280          | 53.4            | 53.4             | 71.1       | 12.3            |      | 77.2       | 117.7         |
| [YOLOv5x6](https://github.com/ultralytics/yolov5/releases)   | 1280          | **54.4**        | **54.4**         | **72.0**   | 22.4            |      | 141.8      | 222.9         |
| [YOLOv5x6](https://github.com/ultralytics/yolov5/releases) TTA | 1280          | **55.0**        | **55.0**         | **72.0**   | 70.8            |      | -          | -             |


[img](https://github.com/ultralytics/yolov5/releases/download/v1.0/model_plot.png)


3. 네트워크 구조
[img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbcD1Ts%2FbtqKBPsHQGp%2FKu8dlxjrsyWFbcjv6XMnqk%2Fimg.png)

- Layer
    - 24 Convolution layers: 이미지 특징 추출
    - 2 Fully-connected layers: 클래스 확률, bounding box 좌표 예측
- '1 x 1 reduction layer' + '3 x 3 convolution layer' GoogLeNet의 네트워크에서 인셉션 구조 대신 사용
- 최종 output(prediction tensors): 7 x 7 x 30


4. 학습
- Convolution/Fully-connected layer
    - ImageNet 데이터셋으로 YOLO 앞단의 20개 Convolution layer를 사전 훈련
    - 사전 훈련된 20개의 Convolution layer 뒤에 4개의 Convolution layer 및 2개의 Fully-connected layer를 추가
- Activation function
    - 모든 계층에 leaky ReLU
    - 마지막 계층: linear activation function
    
- 학습시 보완점
    - confidence score=0, imbalance issue
        - 이미지 전체를 보고 판단하는 방식이라, 대부분의 그리드 셀 내에는 객체가 없다.
        - 이를 보완하기 위해서, 객체가 존재하지 않는 bounding box의 confidence loss에 대한 가중치 감소
        - localization loss, classification loss의 가중치 조절
            - localization loss 가중치 증가
        - 객체가 없는 그리드 셀의 confidence loss보다 객체가 존재하는 그리드 셀의 confidence loss 가중치 증가
    - bounding box size issue
        - 물체의 크기에 따라 bounding box size가 다르게 계산됨
        - 작은 bounding box는 큰 박스에 비해서 위치 변화에 민감
        - scaling 으로 해결
            - bounding box에 Square root 취해주기
            - 높이와 너비가 커짐에 따라 그 증가율이 감소해 loss에 대한 가중치를 감소시키는 효과가 있음
            

5. YOLO 모델의 한계점
- 작은 객체들이 몰려있는 경우 검출이 잘 안됨
- 훈련단계에서 학습하지 못한 박스의 종횡비(aspect ratio)는 잘 예측 안됨


### Focus cam 적용
- 한계점 및 조심할 점!
    - 사람의 얼굴이 뭉개지는 등의 문제로 인식 자체가 안되는 경우가 있음
    - 연예인들의 공연영상마다 의상이 달라서 전체 사이즈(사람 크기)로 학습이 어려움
    - 포지션 등의 보완 방법이 있으나, 이는 이미 무대를 알고 있어야 한다는 한계점이 있음

- 학습시 한계 및 tip
    - image agumentation이 큰 효과를 보지 못함
        - low quality
        - blur..
    - 보다 고화질의 얼굴 이미지가 학습이 더 잘되었음

- 예측시 한계 및 tip
    - input image size = predict image size 맞춰주기
    - threshold 값을 조절해서 backgound 인식을 낮춰줄 필요가 있음



# 5. 웹
[Web Application Sever Structrue](https://raw.githubusercontent.com/kkogggokk/Fproject/main/web/static/images/WAS%20structure.png)


```bash
├── app
│     ├── library
│     │    └── helpers.py      - 비정제, 정제, temp (-> 추론 데이터)
│     ├── pages                - 각 모델별(VGG, MobilNetV2, LSTM) 생성 파일
│     │    ├── home.md         - 비정제, 정제, temp (-> 추론 데이터)
│     │    ├── profile.md      - 비정제, 정제, temp (-> 추론 데이터)
│     │    └── readme.md       - 비정제, 정제, temp (-> 추론 데이터)
│     └── preprocessing.py     - 학습 데이터 생성 file
├── static
│     ├── css
│     ├── images
│     ├── js
│     └── videos
├── templates
│     ├── include
│     ├── base.html
│     └── page.html
```
 
> -  한계점
> 1. 실시간 추론 불가 (시간이 오래 걸린다) + 변수가 너무 많아서 알고리즘으로 정확한 결과추출 한계 , 얼굴을 구별할 수 없는 경우 발생하는 null값 실시간으로 채우기 힘듬
> 2. 댄서를 멤버로 예측하는 경우 발생 (학습 데이터 양 늘리면 해결 될까?)
> 3. 다른 그룹 예측 불가 (재사용성 ? 대체 단어가 …)
