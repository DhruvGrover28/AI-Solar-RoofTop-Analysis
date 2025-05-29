# analysis/image_segmentation.py
import numpy as np
import cv2
from PIL import Image

def segment_rooftop(image: Image.Image, gsd_meters_per_pixel: float = None):
    img_np = np.array(image.convert('RGB'))
    original_height, original_width, _ = img_np.shape
    
    processed_size = (512, 512)
    img_resized = cv2.resize(img_np, processed_size)

    hsv_img = cv2.cvtColor(img_resized, cv2.COLOR_RGB2HSV)
    lower_teal = np.array([75, 50, 50])
    upper_teal = np.array([105, 255, 255])
    mask_color = cv2.inRange(hsv_img, lower_teal, upper_teal)

    gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)
    _, mask_gray = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    if np.sum(mask_color) > (processed_size[0] * processed_size[1] / 10):
        mask = mask_color
    else:
        mask = mask_gray

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)

    usable_area_m2 = 0
    largest_cc_mask = np.zeros_like(mask)

    if num_labels > 1:
        largest_label_idx = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        largest_cc_mask[labels == largest_label_idx] = 255

        if gsd_meters_per_pixel is None:
            area_per_pixel_in_processed_image = 0.01
            usable_area_m2 = np.sum(largest_cc_mask == 255) * area_per_pixel_in_processed_image * 0.7
        else:
            pixel_area_in_original_scale = (gsd_meters_per_pixel * (original_width / processed_size[0])) * \
                                             (gsd_meters_per_pixel * (original_height / processed_size[1]))
            usable_area_m2 = np.sum(largest_cc_mask == 255) * pixel_area_in_original_scale * 0.7

    total_mask_pixels = np.sum(mask == 255)
    largest_cc_pixels = np.sum(largest_cc_mask == 255)

    if total_mask_pixels > 0:
        connected_component_ratio = largest_cc_pixels / total_mask_pixels
    else:
        connected_component_ratio = 0.0

    edges = cv2.Canny(largest_cc_mask, 50, 150)
    edge_pixel_count = np.sum(edges > 0)

    if largest_cc_pixels > 0:
        ideal_perimeter_approx = 4 * np.sqrt(largest_cc_pixels)
        edge_quality_score = min(edge_pixel_count / ideal_perimeter_approx, 1.0)
    else:
        edge_quality_score = 0.0

    confidence = (connected_component_ratio * 0.6) + (edge_quality_score * 0.4)
    confidence = np.clip(confidence, 0.0, 1.0)

    segmented_rgb_mask = Image.fromarray(cv2.cvtColor(largest_cc_mask, cv2.COLOR_GRAY2RGB))

    return segmented_rgb_mask, usable_area_m2, confidence