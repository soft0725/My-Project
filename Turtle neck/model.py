import cv2, torch

def angle(image, ear, number7):  # 비율 조정
    image = image
    height, width, _ = image.shape  # 678, 496

    try:
        angle_height = abs(ear[0][1] - number7[0][1])
        angle_width = abs(ear[0][0] - number7[0][0])

        height = 1022
        width = 1920

        print("-" * 20)
        print("before")
        print(f"angle_height : {angle_height}, height : {height}")
        print(f"angle_width : {angle_width}, width : {width}")

        if height > width:
            print(f"(width / height) : {width / height}")
            height = (width / height) * height
            angle_height = angle_height * (width / height)
        else:
            print(f"(height / width) : {height / width}")
            width = (height / width) * width
            angle_width = angle_width * (height / width)

        print("\nafter")
        print(f"angle_height : {angle_height}, height : {height}")
        print(f"angle_width : {angle_width}, width : {width}")

        print(f"re : {angle_height / angle_width}")

        return angle_height / angle_width

    except IndexError as e:
        return False

def draw(image, ear, number7):
    red = (0, 0, 255)

    print(f"draw ear : {ear}")
    print(f"draw number : {number7}")

    try:
        cv2.circle(image, (ear[0][0], ear[0][1]), 5, red, -1)  # 귀 부분에 마킹
        cv2.circle(image, (number7[0][0], number7[0][1]), 5, red, -1)  # 경추7번 부분에 마킹
        cv2.line(image, (ear[0][0], ear[0][1]), (number7[0][0], number7[0][1]), red, 2)  # 귀에서 경추7번 까지 직선
        cv2.line(image, (ear[0][0], number7[0][1]), (number7[0][0], number7[0][1]), red, 2)  # 경추7번에서 수평으로 직선
    except IndexError as e:
        print(f"{e}")
        print("위 출력값 확인 필요")

    return image

def main():
    image = cv2.imread('images/uploaded_image.jpg')
    weight = 'Version_1.pt'

    model = torch.hub.load('ultralytics/yolov5', 'custom', weight, force_reload=True)
    result = model(image)
    predictions = result.pandas().xyxy[0]
    ear = []
    number7 = []

    for _, row in predictions.iterrows():
        label = row['name']  # 라벨명
        confidence = row['confidence']  # 정확도
        bbox = row[['xmin', 'ymin', 'xmax', 'ymax']].values
        x_min, y_min, x_max, y_max = bbox.astype(int)  # 박스 모서리 좌표
        if confidence > 0.51111:
            if label == 'ear':  # 귀에 대한 좌푯값
                x = (x_min + x_max) // 2
                y = (y_min + y_max) // 2
                if x and y:
                    print("귀 측정 문제 X")
                    ear.append([x, y])
                else:
                    print("귀가 보이질 않거나 가려져 있습니다.")
            elif label == 'number7':
                x = (x_min + x_max) // 2
                y = (y_min + y_max) // 2
                if x and y:
                    print("경추7번 측정 문제 X")
                    number7.append([x, y])
                else:
                    print("경추 7번이 보이질 않거나 가려져 있습니다.")

    image = draw(image, ear, number7)
    result = angle(image, ear, number7)

    cv2.imwrite('images/Result.jpg', image)

    if result:
        return result
    else:
        return False

if __name__ == "__main__":
    main()