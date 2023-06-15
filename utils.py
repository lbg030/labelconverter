import json
import cv2
import os


def labelme2hubble(json_data, file_name, class_list):
    hubble_set = [
        {
            'defectTypeName': shape['label'],
            'data': {
                'coordinateList': [
                    list(map(int, shape['points'][0])),
                    [int(shape['points'][1][0]), int(shape['points'][0][1])],
                    list(map(int, shape['points'][1])),
                    [int(shape['points'][0][0]), int(shape['points'][1][1])]
                ]
            }
        }
        for shape in json_data['shapes']
    ]

    dir_name, base_name = os.path.split(file_name)
    new_dir = os.path.join(dir_name, "hubble_json")
    os.makedirs(new_dir, exist_ok=True)  # Make sure the directory exists
    new_file_name = os.path.join(new_dir, base_name)

    with open(new_file_name, 'w') as w_file:
        json.dump(hubble_set, w_file, indent=4)


def convert(size, box, label):
    c = label
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return f"{c} {x} {y} {w} {h}"


def labelme2yolo(data, file_path, class_list):
    defect_label = {class_list[i]: i for i in range(len(class_list))}
    # Use os.path.splitext to remove the extension
    txt_file_name = os.path.splitext(file_path)[0] + '.txt'

    w = int(data['imageWidth'])
    h = int(data['imageHeight'])

    lines = []
    for shape in data['shapes']:
        label = defect_label[shape['label']]
        points = shape['points']

        xmin = min(points[0][0], points[1][0])
        ymin = min(points[0][1], points[1][1])
        xmax = max(points[0][0], points[1][0])
        ymax = max(points[0][1], points[1][1])

        b = (xmin, xmax, ymin, ymax)
        line = convert((w, h), b, label)
        lines.append(line)

    with open(txt_file_name, "w") as f:
        f.write('\n'.join(lines))


def yolo2labelme(file_path, class_list):
    def convert_yolo_to_labelme(txt_file_path, img_file_path, labelme_file_path):
        with open(txt_file_path, 'r') as f:
            yolo_lines = f.readlines()

        label_dict = {class_list[i]: int(i) for i in range(len(class_list))}
        img = cv2.imread(img_file_path)
        height, width, channels = img.shape

        labelme_data = {
            "version": "4.5.7",
            "flags": {},
            "shapes": [],
            # Use os.path.basename to get the file name from a path
            "imagePath": os.path.basename(img_file_path),
            "imageData": None,
            "imageWidth": width,
            "imageHeight": height,
        }

        for line in yolo_lines:
            label, x_center, y_center, box_width, box_height = line.strip().split(' ')
            x_center, y_center, box_width, box_height = map(
                float, (x_center, y_center, box_width, box_height))
            x1 = (x_center - box_width / 2) * width
            y1 = (y_center - box_height / 2) * height
            x2 = (x_center + box_width / 2) * width
            y2 = (y_center + box_height / 2) * height

            shape = {
                "label": next(k for k, v in label_dict.items() if v == int(label)),
                "points": [[x1, y1], [x2, y2]],
                "group_id": None,
                "shape_type": "rectangle",
                "flags": {}
            }

            labelme_data["shapes"].append(shape)

        with open(labelme_file_path, 'w') as f:
            json.dump(labelme_data, f, indent=4)

    # Use os.path.splitext to split the file name and the extension
    name, ext = os.path.splitext(file_path)
    convert_yolo_to_labelme(name + '.txt', name + '.png', name + '.json')