import skimage.transform
import math

def transform_and_pad_image(
    image,
    target_width,
    target_height,
    scale=None,
    rotation=None,
    shift=None,
    order=1,
    mode="edge",
):
    """
    Transform image and pad by edge pixles.
    """
    image_width = image.shape[1]
    image_height = image.shape[0]
    image_array = image

    # centerize
    t = skimage.transform.AffineTransform(
        translation=(-image_width * 0.5, -image_height * 0.5)
    )

    if scale:
        t += skimage.transform.AffineTransform(scale=(scale, scale))

    if rotation:
        radian = (rotation / 180.0) * math.pi
        t += skimage.transform.AffineTransform(rotation=radian)

    t += skimage.transform.AffineTransform(
        translation=(target_width * 0.5, target_height * 0.5)
    )

    if shift:
        t += skimage.transform.AffineTransform(
            translation=(target_width * shift[0], target_height * shift[1])
        )

    warp_shape = (target_height, target_width)

    image_array = skimage.transform.warp(
        image_array, (t).inverse, output_shape=warp_shape, order=order, mode=mode
    )

    return image_array