from skimage.measure import shannon_entropy
import cv2
import numpy as np


def compute_local_variance(image, ksize=5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mean = cv2.blur(gray, (ksize, ksize))
    squared_mean = cv2.blur(gray**2, (ksize, ksize))
    variance = squared_mean - (mean**2)
    return np.mean(variance)


def compute_entropy(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return -1.*shannon_entropy(gray)


def compute_tenengrad(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)  # Sobel filter in X direction
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)  # Sobel filter in Y direction
    tenengrad = np.sqrt(sobel_x**2 + sobel_y**2)  # Compute gradient magnitude
    return -1.*np.mean(tenengrad)  # Return mean gradient magnitude as focus score

	
def compute_brenner_gradient(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    shifted = np.roll(gray, -2, axis=1)  # Shift by 2 pixels horizontally
    diff = (gray - shifted) ** 2  # Compute squared difference
    return -1.*np.sum(diff)  # Sum all differences as the focus measure


def compute_sobel_variance(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)  # Sobel X gradient
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)  # Sobel Y gradient
    sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)  # Compute gradient magnitude
    variance = np.var(gray)  # Compute variance of pixel intensities
    return np.mean(sobel_magnitude) + variance  # Combine Sobel and variance


def compute_laplacian(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)  # Apply Laplacian filter
    return -1.*np.var(laplacian)  # Compute variance of Laplacian