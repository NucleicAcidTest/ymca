import math


def main():
    x1, y1, r1 = map(float, input().split())
    x2, y2, r2 = map(float, input().split())

    distance = math.hypot(x2 - x1, y2 - y1)

    if distance >= r1 + r2:
        area = 0.0
    elif distance <= abs(r1 - r2):
        radius = min(r1, r2)
        area = math.pi * radius * radius
    else:
        angle1 = 2 * math.acos((distance * distance + r1 * r1 - r2 * r2) / (2 * distance * r1))
        angle2 = 2 * math.acos((distance * distance + r2 * r2 - r1 * r1) / (2 * distance * r2))

        area1 = 0.5 * r1 * r1 * (angle1 - math.sin(angle1))
        area2 = 0.5 * r2 * r2 * (angle2 - math.sin(angle2))
        area = area1 + area2

    print(f"{area:.6f}")


if __name__ == "__main__":
    main()
