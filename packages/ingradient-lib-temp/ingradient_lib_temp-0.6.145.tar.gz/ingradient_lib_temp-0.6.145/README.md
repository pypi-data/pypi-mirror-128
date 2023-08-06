# ingradient library
 
## 0. 다운로드
pip install ingradient-lib-temp

## 1. 이미지 포멧 맞추기 (Data Organizer
![스크린샷 2021-09-23 오후 4 36 04](https://user-images.githubusercontent.com/87344797/134470205-83603804-7556-402c-833a-1b919b7a16db.png)
- 위와 같은 구성을 따른다.
- 인덱싱에 딱히 기준은 없으나 데이터 파일들을 npz파일과 pkl파일로 나눈 후, sorting해서 순서대로 dataset에서 가져오므로 npz파일과 pkl파일은 같은 순번을 따르도록 한다.

![스크린샷 2021-09-26 오전 2 37 03](https://user-images.githubusercontent.com/87344797/134780921-c2d348a8-704c-4fad-bb02-9f1570268932.png)
- Data Organizer를 이용해 쉽게 정리할 수 있다.
- Multi Modality일 경우 img_path_list에 각 modality에 해당하는 주소를 입력한다.
- 그 후, Modality 변수에 modality 정보를 입력한다. 예시) modality = ['T1', 'T2'. 'T1-CE', 'FLAIR']
            

## 2. Resampling
![스크린샷 2021-09-23 오후 4 58 09](https://user-images.githubusercontent.com/87344797/134472713-eef1a815-a090-4575-b30b-cf28e726e332.png)

- Get_target_spacing 객체를 만든다.
- 이 때 Anisotropy Threshold 값을 고를 수 있다 Default 값은 3이다. 이 외에도 isotropy_percentile_value = 0.50, anisotropy_percentile_value = 0.90에 Default가 맞춰져 있다. 이를 변경하는 것도 가능하다.
- run 메소드를 사용해 Dataset들이 저장된 폴더로부터 Spacing 값들을 구한다. 이 떄 각 spacing 값들이 해당 객체안에 저장된다.
- Target Spacing값과 Anisotropy axis에 해당하는 index를 얻는다.
- 해당 값들을 Resampling 객체를 만들 때 넣어준다.
- 뒤에 이 Resampling 객체는 DataLoader에 들어가게 되며, 이 후 자동으로 patch 단위로 Resampling을 진행한다.


## 3. Normalizer
![스크린샷 2021-09-23 오후 5 00 30](https://user-images.githubusercontent.com/87344797/134472958-d024dce0-c524-4fb9-9e4d-24c9f8a9d30a.png)

- Normalizer를 생성한다. 생성 시에 percentile clipping 값을 설정할 수 있다.
- nnUNet의 기본 세팅은 MRI의 경우 percentile clipping을 사용하지 않고, CT의 경우 [0.05, 0.95]를 따른다.
- 이 후, dataset 메소드에서 normalizer를 가져와 데이터를 샘플링 할 때 마다 한 patient 단위로 normalization을 수행한다.

## 4.Data Augmentation
![스크린샷 2021-09-27 오전 1 29 03](https://user-images.githubusercontent.com/87344797/134816035-53001b25-fcc9-45d5-8bec-17ae5887fd4d.png)
- patch_transform에서 어그멘테이션 메소드를 가져와 transform에 추가한다. Transform([연산1, 연산2, ...], [연산1 실행확률, 연산2 실행확률, ...]) 이다.
- 또는 get_nnunet_setting에서 nnunet 세팅을 가져올 수 있다. get_transform_param의 input은 GPU device index다


## 5. Dataset
![스크린샷 2021-09-27 오전 1 30 24](https://user-images.githubusercontent.com/87344797/134816067-a487fd28-69ff-4832-8c0d-6ed2e70da03d.png)
- CustomDataset은 torch.utils.data에서 dataset 클래스를 상속 받았다. 때문에 pytorch의 random split 연산을 사용할 수 있다.
- 데이터 셋이 저장된 디렉토리의 PATH를 입력한다.
- 이전에 선언한 normalizer와 resampling을 진행한다.

## 5. DataLoader
![스크린샷 2021-09-27 오전 1 31 19](https://user-images.githubusercontent.com/87344797/134816080-8cba89c6-3248-4a4f-8619-440c4fad1a3f.png)
- Batch Size는 하나의 Patient에서 뽑아내게 되며 기본적으로 nnUNet이 사용한 Oversampling이 지원된다.
- iteration은 각 patient별로 몇번의 샘플링을 진행할 지 정한다. 만약 batch size = 2, iteration = 2 라면 1epoch 마다 하나의 patient에서 4번의 샘플링을 진행한다.
- transform을 추가한다.


## 6. Deep Supervision Model
![스크린샷 2021-09-23 오후 5 46 09](https://user-images.githubusercontent.com/87344797/134478620-21c9d460-0158-4080-a475-bd6fdaa0a224.png)

![스크린샷 2021-09-23 오후 5 12 56](https://user-images.githubusercontent.com/87344797/134474469-5feaca9b-45d6-4a2d-be3e-b68d7dadc14b.png)

- nnUNet에서 사용한 Deep supervision model을 기본적으로 지원한다.
- Loss 역시 연산 식이 기존과 다르므로 지원한다.

## 7. Trainer & Tensor board
![스크린샷 2021-09-27 오전 1 29 34](https://user-images.githubusercontent.com/87344797/134816046-05f38ccf-9471-4098-90f4-cf1e5e4343e4.png)
- 위와 같이 실행한다.
- 텐서보드 지원

## 8. Inference
![스크린샷 2021-09-23 오후 5 14 30](https://user-images.githubusercontent.com/87344797/134474697-2e4da734-4704-4724-ab84-4009f820c0f0.png)

- dataset에 대해 Inference를 진행한다. dataset은 CustomDataset에 해당하는 모듈이다.
- mode = 'save' 일 경우 결과물을 save_path에 저장한다. mode = 'dice' 일 경우 각 파일들의 dice score를 print 한다.


## 9. Visualization
![스크린샷 2021-09-23 오후 5 16 42](https://user-images.githubusercontent.com/87344797/134475015-244de41f-b097-4eba-b3fb-5ff2469df5d1.png)
- Training 시에 Segmentation Output을 각 Deepsupervision Layer 별로 지원한다.
- 이 외에도 기본 plain unet에 대한 시각화도 지원한다.





