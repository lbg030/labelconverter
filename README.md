# LabelConverter

## 요구사항 (Requirements)

This project requires the following packages:

- json
- opencv-python

## 기능 (Features)

The current available features in this project include:

- Labelme2Yolo
- Labelme2Hubble
- Yolo2Labelme

The features yet to be implemented are:

- [ ] Lens2Hubble

## 버전 (Version)

The current version is `0.1.0`.

## 사용 방법 (Usage)

1. Run the `labelconverter.exe` file.
2. Set your desired format in Format Type.
3. Click the 'Select Directory' button and navigate to the folder you want to convert. However, you must navigate to a folder where the class name exists.
    - Example: If you have a folder structure as below, you should select the `Animal` folder.
    ```
    Animal
    └── bear
    │   └── bear.png
    └── dog
    │   └── dog.png
    └── cat
        └── cat.png
    ```
4. Click the 'Convert format' button to change to the desired format.

