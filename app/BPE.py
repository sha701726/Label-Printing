import cv2

drawing = False
ix, iy = -1, -1

# Store all rectangles
rectangles = []

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, img, temp_img

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            temp_img = img.copy()
            cv2.rectangle(temp_img, (ix, iy), (x, y), (0, 255, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

        # Handle drag in any direction
        x_start = min(ix, x)
        y_start = min(iy, y)
        w = abs(x - ix)
        h = abs(y - iy)

        rectangles.append((x_start, y_start, w, h))

        print(f"ROI: x={x_start}, y={y_start}, w={w}, h={h}")

        # Draw final rectangle
        cv2.rectangle(img, (x_start, y_start), (x_start + w, y_start + h), (0, 255, 0), 2)


# Load image (NO RESIZE)
img = cv2.imread("test2.jpeg")

if img is None:
    print("Error: Image not found")
    exit()

temp_img = img.copy()

# Use WINDOW_NORMAL for better handling
cv2.namedWindow("Draw ROIs", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Draw ROIs", draw_rectangle)

print("Instructions:")
print("- Drag mouse to draw rectangle")
print("- Multiple rectangles allowed")
print("- Press 'r' to reset")
print("- Press ESC to exit\n")

while True:
    if drawing:
        cv2.imshow("Draw ROIs", temp_img)
    else:
        cv2.imshow("Draw ROIs", img)

    key = cv2.waitKey(1) & 0xFF

    # Reset screen
    if key == ord('r'):
        img = cv2.imread("test2.jpeg")  # reload original size
        temp_img = img.copy()
        rectangles.clear()
        print("\nReset all rectangles\n")

    # Exit
    elif key == 27:
        break

cv2.destroyAllWindows()

print("\nAll ROIs:")
for i, rect in enumerate(rectangles):
    print(f"{i+1}: {rect}")