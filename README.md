# Label Converter

Label Converter는 다양한 포맷 간에 레이블 데이터를 변환하는 유틸리티입니다.

## Requirements

- Python 3.5 이상
- 패키지 설치: `pip install -r requirements.txt`

```json
{
  "opencv-python": "^4.5.3",
  "json": "^2.0.9"
}
```

## Features
Labelme2Yolo: Labelme JSON 형식의 레이블을 YOLO 형식으로 변환합니다.
Labelme2Hubble: Labelme JSON 형식의 레이블을 Hubble 형식으로 변환합니다.
Yolo2Labelme: YOLO 형식의 레이블을 Labelme JSON 형식으로 변환합니다.
Lens2Hubble: (TODO) Lens 형식의 레이블을 Hubble 형식으로 변환합니다.

## Version
현재 버전: 0.1.0

## Usage
1) labelconverter.exe 파일을 실행합니다.

2) Format Type에서 원하는 포맷으로 설정합니다.

3) Select Directory 버튼을 클릭하여 레이블을 변환하고자 하는 폴더로 이동합니다. 다만, 클래스명이 존재하는 폴더로 이동해야 합니다.

예시:

bash
Copy code
Animal
├── bear
│   └── bear.png
├── dog
│   └── dog.png
└── cat
    └── cat.png
위의 예시에서는 "Animal" 폴더를 선택해야 합니다.

4) Convert format 버튼을 눌러 원하는 포맷으로 레이블을 변경합니다.
