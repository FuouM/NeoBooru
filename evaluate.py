from typing import Any, Iterable, List, Tuple, Union
import six
import tensorflow as tf
import tensorflow_io as tfio
from image_processing import transform_and_pad_image

def load_image_for_evaluate(
    input_: Union[str, six.BytesIO], width: int, height: int, normalize: bool = True
) -> Any:
    if isinstance(input_, six.BytesIO):
        image_raw = input_.getvalue()
    else:
        image_raw = tf.io.read_file(input_)
    try:
        image = tf.io.decode_png(image_raw, channels=3)
    except:
        image = tfio.image.decode_webp(image_raw)
        image = tfio.experimental.color.rgba_to_rgb(image)

    image = tf.image.resize(
        image,
        size=(height, width),
        method=tf.image.ResizeMethod.AREA,
        preserve_aspect_ratio=True,
    )
    image = image.numpy()  # EagerTensor to np.array
    image = transform_and_pad_image(image, width, height)

    if normalize:
        image = image / 255.0

    return image


def evaluate_image(
    image_input: Union[str, six.BytesIO], model: Any, tags: List[str], threshold: float
) -> Iterable[Tuple[str, float]]:
    width, height = model.input_shape[2], model.input_shape[1]
    
    image = load_image_for_evaluate(image_input, width=width, height=height)
    image_shape = image.shape
    image = image.reshape((1, image_shape[0], image_shape[1], image_shape[2]))
    y = model.predict(image)[0]
    results = [(tags[i], y[i]) for i in range(len(tags))]

    return [(tag, score) for tag, score in results if score >= threshold]