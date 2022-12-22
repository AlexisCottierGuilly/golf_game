from concurrent.futures import ThreadPoolExecutor

import PIL, np

# Create Mandelbrot fractal

def mandelbrot(x, y, max_iters):
    """Given the real and imaginary parts of a complex number,
    determine if it is a candidate for membership in the Mandelbrot
    set given a fixed number of iterations.
    """
    c = complex(x, y)
    z = 0.0j
    for i in range(max_iters):
        z = z * z + c
        if (z.real * z.real + z.imag * z.imag) >= 4:
            return i

    return max_iters

def create_fractal(min_x, max_x, min_y, max_y, image, iters, num_threads=1):
    """Create a fractal image using the Mandelbrot algorithm."""
    height = image.shape[0]
    width = image.shape[1]

    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        y_coords = np.linspace(min_y, max_y, height)
        for x in range(width):
            x_coord = min_x + x * pixel_size_x
            executor.map(mandelbrot, [x_coord] * height, y_coords, [iters] * height, [image[:, x]] * height)

if __name__ == '__main__':
    image = np.zeros((1024, 1536), dtype=np.uint8)
    create_fractal(-2.0, 1.0, -1.0, 1.0, image, 20, num_threads=4)
    img = PIL.Image.fromarray(image)
    img.show()