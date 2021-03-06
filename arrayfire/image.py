#######################################################
# Copyright (c) 2015, ArrayFire
# All rights reserved.
#
# This file is distributed under 3-clause BSD license.
# The complete license agreement can be obtained at:
# http://arrayfire.com/licenses/BSD-3-Clause
########################################################

"""
Image processing functions for arrayfire.
"""

from .library import *
from .array import *
from .data import constant
import os

def gradient(image):
    """
    Find the horizontal and vertical gradients.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image, or
          - A multi dimensional array representing batch of images.

    Returns
    ---------
    (dx, dy) : Tuple of af.Array.
             - `dx` containing the horizontal gradients of `image`.
             - `dy` containing the vertical gradients of `image`.

    """
    dx = Array()
    dy = Array()
    safe_call(backend.get().af_gradient(ct.pointer(dx.arr), ct.pointer(dy.arr), image.arr))
    return dx, dy

def load_image(file_name, is_color=False):
    """
    Load an image on the disk as an array.

    Parameters
    ----------
    file_name: str
          - Full path of the file name on disk.

    is_color : optional: bool. default: False.
          - Specifies if the image is loaded as 1 channel (if False) or 3 channel image (if True).

    Returns
    -------
    image - af.Array
            A 2 dimensional (1 channel) or 3 dimensional (3 channel) array containing the image.

    """
    assert(os.path.isfile(file_name))
    image = Array()
    safe_call(backend.get().af_load_image(ct.pointer(image.arr),
                                          ct.c_char_p(file_name.encode('ascii')), is_color))
    return image

def save_image(image, file_name):
    """
    Save an array as an image on the disk.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image.

    file_name: str
          - Full path of the file name on the disk.
    """
    assert(isinstance(file_name, str))
    safe_call(backend.get().af_save_image(ct.c_char_p(file_name.encode('ascii')), image.arr))
    return image

def resize(image, scale=None, odim0=None, odim1=None, method=INTERP.NEAREST):
    """
    Resize an image.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image, or
          - A multi dimensional array representing batch of images.

    scale : optional: scalar. default: None.
          - Scale factor for the image resizing.

    odim0 : optional: int. default: None.
          - Size of the first dimension of the output.

    odim1 : optional: int. default: None.
          - Size of the second dimension of the output.

    method : optional: af.INTERP. default: af.INTERP.NEAREST.
          - Interpolation method used for resizing.

    Returns
    ---------
    out  : af.Array
          - Output image after resizing.

    Note
    -----

    - If `scale` is None, `odim0` and `odim1` need to be specified.
    - If `scale` is not None, `odim0` and `odim1` are ignored.

    """
    if (scale is None):
        assert(odim0 is not None)
        assert(odim1 is not None)
    else:
        idims = image.dims()
        odim0 = int(scale * idims[0])
        odim1 = int(scale * idims[1])

    output = Array()
    safe_call(backend.get().af_resize(ct.pointer(output.arr),
                                      image.arr, ct.c_longlong(odim0),
                                      ct.c_longlong(odim1), method.value))

    return output

def transform(image, trans_mat, odim0 = 0, odim1 = 0, method=INTERP.NEAREST, is_inverse=True):
    """
    Transform an image using a transformation matrix.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image, or
          - A multi dimensional array representing batch of images.

    trans_mat : af.Array
          - A 2 D floating point arrayfire array of size [3, 2].

    odim0 : optional: int. default: 0.
          - Size of the first dimension of the output.

    odim1 : optional: int. default: 0.
          - Size of the second dimension of the output.

    method : optional: af.INTERP. default: af.INTERP.NEAREST.
          - Interpolation method used for transformation.

    is_inverse : optional: bool. default: True.
          - Specifies if the inverse transform is applied.

    Returns
    ---------
    out  : af.Array
          - Output image after transformation.

    Note
    -----

    - If `odim0` and `odim` are 0, the output dimensions are automatically calculated by the function.

    """
    output = Array()
    safe_call(backend.get().af_transform(ct.pointer(output.arr),
                                         image.arr, trans_mat.arr,
                                         ct.c_longlong(odim0), ct.c_longlong(odim1),
                                         method.value, is_inverse))
    return output

def rotate(image, theta, is_crop = True, method = INTERP.NEAREST):
    """
    Rotate an image.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image, or
          - A multi dimensional array representing batch of images.

    theta : scalar
          - The angle to rotate in radians.

    is_crop : optional: bool. default: True.
          - Specifies if the output should be cropped to the input size.

    method : optional: af.INTERP. default: af.INTERP.NEAREST.
          - Interpolation method used for rotating.

    Returns
    ---------
    out  : af.Array
          - Output image after rotating.
    """
    output = Array()
    safe_call(backend.get().af_rotate(ct.pointer(output.arr), image.arr,
                                      ct.c_double(theta), is_crop, method.value))
    return output

def translate(image, trans0, trans1, odim0 = 0, odim1 = 0, method = INTERP.NEAREST):
    """
    Translate an image.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image, or
          - A multi dimensional array representing batch of images.

    trans0: int.
          - Translation along first dimension in pixels.

    trans1: int.
          - Translation along second dimension in pixels.

    odim0 : optional: int. default: 0.
          - Size of the first dimension of the output.

    odim1 : optional: int. default: 0.
          - Size of the second dimension of the output.

    method : optional: af.INTERP. default: af.INTERP.NEAREST.
          - Interpolation method used for translation.

    Returns
    ---------
    out  : af.Array
          - Output image after translation.

    Note
    -----

    - If `odim0` and `odim` are 0, the output dimensions are automatically calculated by the function.

    """
    output = Array()
    safe_call(backend.get().af_translate(ct.pointer(output.arr),
                                         image.arr, trans0, trans1,
                                         ct.c_longlong(odim0), ct.c_longlong(odim1), method.value))
    return output

def scale(image, scale0, scale1, odim0 = 0, odim1 = 0, method = INTERP.NEAREST):
    """
    Scale an image.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image, or
          - A multi dimensional array representing batch of images.

    scale0 : scalar.
          - Scale factor for the first dimension.

    scale1 : scalar.
          - Scale factor for the second dimension.

    odim0 : optional: int. default: None.
          - Size of the first dimension of the output.

    odim1 : optional: int. default: None.
          - Size of the second dimension of the output.

    method : optional: af.INTERP. default: af.INTERP.NEAREST.
          - Interpolation method used for resizing.

    Returns
    ---------
    out  : af.Array
          - Output image after scaling.

    Note
    -----

    - If `odim0` and `odim` are 0, the output dimensions are automatically calculated by the function.

    """
    output = Array()
    safe_call(backend.get().af_scale(ct.pointer(output.arr),
                                     image.arr, ct.c_double(scale0), ct.c_double(scale1),
                                     ct.c_longlong(odim0), ct.c_longlong(odim1), method.value))
    return output

def skew(image, skew0, skew1, odim0 = 0, odim1 = 0, method = INTERP.NEAREST, is_inverse=True):
    """
    Skew an image.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image, or
          - A multi dimensional array representing batch of images.

    skew0 : scalar.
          - Skew factor for the first dimension.

    skew1 : scalar.
          - Skew factor for the second dimension.

    odim0 : optional: int. default: None.
          - Size of the first dimension of the output.

    odim1 : optional: int. default: None.
          - Size of the second dimension of the output.

    method : optional: af.INTERP. default: af.INTERP.NEAREST.
          - Interpolation method used for resizing.

    is_inverse : optional: bool. default: True.
          - Specifies if the inverse skew  is applied.

    Returns
    ---------
    out  : af.Array
          - Output image after skewing.

    Note
    -----

    - If `odim0` and `odim` are 0, the output dimensions are automatically calculated by the function.

    """
    output = Array()
    safe_call(backend.get().af_skew(ct.pointer(output.arr),
                                    image.arr, ct.c_double(skew0), ct.c_double(skew1),
                                    ct.c_longlong(odim0), ct.c_longlong(odim1),
                                    method.value, is_inverse))

    return output

def histogram(image, nbins, min_val = None, max_val = None):
    """
    Find the histogram of an image.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image, or
          - A multi dimensional array representing batch of images.

    nbins : int.
          - Number of bins in the histogram.

    min_val : optional: scalar. default: None.
          - The lower bound for the bin values.
          - If None, `af.min(image)` is used.

    max_val : optional: scalar. default: None.
          - The upper bound for the bin values.
          - If None, `af.max(image)` is used.

    Returns
    ---------
    hist : af.Array
          - Containing the histogram of the image.

    """
    from .algorithm import min as af_min
    from .algorithm import max as af_max

    if min_val is None:
        min_val = af_min(image)

    if max_val is None:
        max_val = af_max(image)

    output = Array()
    safe_call(backend.get().af_histogram(ct.pointer(output.arr),
                                         image.arr, ct.c_uint(nbins),
                                         ct.c_double(min_val), ct.c_double(max_val)))
    return output

def hist_equal(image, hist):
    """
    Equalize an image based on a histogram.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image, or
          - A multi dimensional array representing batch of images.

    hist : af.Array
          - Containing the histogram of an image.

    Returns
    ---------

    output : af.Array
           - The equalized image.

    """
    output = Array()
    safe_call(backend.get().af_hist_equal(ct.pointer(output.arr), image.arr, hist.arr))
    return output

def dilate(image, mask = None):
    """
    Run image dilate on the image.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image, or
          - A multi dimensional array representing batch of images.

    mask  : optional: af.Array. default: None.
          - Specifies the neighborhood of a pixel.
          - When None, a [3, 3] array of all ones is used.

    Returns
    ---------

    output : af.Array
           - The dilated image.

    """
    if mask is None:
        mask = constant(1, 3, 3, dtype=Dtype.f32)

    output = Array()
    safe_call(backend.get().af_dilate(ct.pointer(output.arr), image.arr, mask.arr))

    return output

def dilate3(volume, mask = None):
    """
    Run volume dilate on a volume.

    Parameters
    ----------
    volume : af.Array
          - A 3 D arrayfire array representing a volume, or
          - A multi dimensional array representing batch of volumes.

    mask  : optional: af.Array. default: None.
          - Specifies the neighborhood of a pixel.
          - When None, a [3, 3, 3] array of all ones is used.

    Returns
    ---------

    output : af.Array
           - The dilated volume.

    """
    if mask is None:
        mask = constant(1, 3, 3, 3, dtype=Dtype.f32)

    output = Array()
    safe_call(backend.get().af_dilate3(ct.pointer(output.arr), volume.arr, mask.arr))

    return output

def erode(image, mask = None):
    """
    Run image erode on the image.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image, or
          - A multi dimensional array representing batch of images.

    mask  : optional: af.Array. default: None.
          - Specifies the neighborhood of a pixel.
          - When None, a [3, 3] array of all ones is used.

    Returns
    ---------

    output : af.Array
           - The eroded image.

    """
    if mask is None:
        mask = constant(1, 3, 3, dtype=Dtype.f32)

    output = Array()
    safe_call(backend.get().af_erode(ct.pointer(output.arr), image.arr, mask.arr))

    return output

def erode3(volume, mask = None):
    """
    Run volume erode on the volume.

    Parameters
    ----------
    volume : af.Array
          - A 3 D arrayfire array representing an volume, or
          - A multi dimensional array representing batch of volumes.

    mask  : optional: af.Array. default: None.
          - Specifies the neighborhood of a pixel.
          - When None, a [3, 3, 3] array of all ones is used.

    Returns
    ---------

    output : af.Array
           - The eroded volume.

    """

    if mask is None:
        mask = constant(1, 3, 3, 3, dtype=Dtype.f32)

    output = Array()
    safe_call(backend.get().af_erode3(ct.pointer(output.arr), volume.arr, mask.arr))

    return output

def bilateral(image, s_sigma, c_sigma, is_color = False):
    """
    Apply bilateral filter to the image.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image, or
          - A multi dimensional array representing batch of images.

    s_sigma : scalar.
          - Sigma value for the co-ordinate space.

    c_sigma : scalar.
          - Sigma value for the color space.

    is_color : optional: bool. default: False.
          - Specifies if the third dimension is 3rd channel (if True) or a batch (if False).

    Returns
    ---------

    output : af.Array
           - The image after the application of the bilateral filter.

    """
    output = Array()
    safe_call(backend.get().af_bilateral(ct.pointer(output.arr),
                                         image.arr, ct.c_double(s_sigma),
                                         ct.c_double(c_sigma), is_color))
    return output

def mean_shift(image, s_sigma, c_sigma, n_iter, is_color = False):
    """
    Apply mean shift to the image.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image, or
          - A multi dimensional array representing batch of images.

    s_sigma : scalar.
          - Sigma value for the co-ordinate space.

    c_sigma : scalar.
          - Sigma value for the color space.

    n_iter  : int.
          - Number of mean shift iterations.

    is_color : optional: bool. default: False.
          - Specifies if the third dimension is 3rd channel (if True) or a batch (if False).

    Returns
    ---------

    output : af.Array
           - The image after the application of the meanshift.

    """
    output = Array()
    safe_call(backend.get().af_mean_shift(ct.pointer(output.arr),
                                          image.arr, ct.c_double(s_sigma), ct.c_double(c_sigma),
                                          ct.c_uint(n_iter), is_color))
    return output

def medfilt(image, w0 = 3, w1 = 3, edge_pad = PAD.ZERO):
    """
    Apply median filter for the image.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image, or
          - A multi dimensional array representing batch of images.

    w0 : optional: int. default: 3.
          - The length of the filter along the first dimension.

    w1 : optional: int. default: 3.
          - The length of the filter along the second dimension.

    edge_pad : optional: af.PAD. default: af.PAD.ZERO
          - Flag specifying how the median at the edge should be treated.

    Returns
    ---------

    output : af.Array
           - The image after median filter is applied.

    """
    output = Array()
    safe_call(backend.get().af_medfilt(ct.pointer(output.arr),
                                       image.arr, ct.c_longlong(w0),
                                       ct.c_longlong(w1), edge_pad.value))
    return output

def minfilt(image, w_len = 3, w_wid = 3, edge_pad = PAD.ZERO):
    """
    Apply min filter for the image.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image, or
          - A multi dimensional array representing batch of images.

    w0 : optional: int. default: 3.
          - The length of the filter along the first dimension.

    w1 : optional: int. default: 3.
          - The length of the filter along the second dimension.

    edge_pad : optional: af.PAD. default: af.PAD.ZERO
          - Flag specifying how the min at the edge should be treated.

    Returns
    ---------

    output : af.Array
           - The image after min filter is applied.

    """
    output = Array()
    safe_call(backend.get().af_minfilt(ct.pointer(output.arr),
                                       image.arr, ct.c_longlong(w_len),
                                       ct.c_longlong(w_wid), edge_pad.value))
    return output

def maxfilt(image, w_len = 3, w_wid = 3, edge_pad = PAD.ZERO):
    """
    Apply max filter for the image.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image, or
          - A multi dimensional array representing batch of images.

    w0 : optional: int. default: 3.
          - The length of the filter along the first dimension.

    w1 : optional: int. default: 3.
          - The length of the filter along the second dimension.

    edge_pad : optional: af.PAD. default: af.PAD.ZERO
          - Flag specifying how the max at the edge should be treated.

    Returns
    ---------

    output : af.Array
           - The image after max filter is applied.

    """
    output = Array()
    safe_call(backend.get().af_maxfilt(ct.pointer(output.arr),
                                       image.arr, ct.c_longlong(w_len),
                                       ct.c_longlong(w_wid), edge_pad.value))
    return output

def regions(image, conn = CONNECTIVITY.FOUR, out_type = Dtype.f32):
    """
    Find the connected components in the image.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image.

    conn : optional: af.CONNECTIVITY. default: af.CONNECTIVITY.FOUR.
          - Specifies the connectivity of the pixels.

    out_type : optional: af.Dtype. default: af.Dtype.f32.
          - Specifies the type for the output.

    Returns
    ---------

    output : af.Array
           - An array where each pixel is labeled with its component number.

    """
    output = Array()
    safe_call(backend.get().af_regions(ct.pointer(output.arr), image.arr,
                                       conn.value, out_type.value))
    return output

def sobel_derivatives(image, w_len=3):
    """
    Find the sobel derivatives of the image.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image, or
          - A multi dimensional array representing batch of images.

    w_len : optional: int. default: 3.
          - The size of the sobel operator.

    Returns
    ---------

    (dx, dy) : tuple of af.Arrays.
           - `dx` is the sobel derivative along the horizontal direction.
           - `dy` is the sobel derivative along the vertical direction.

    """
    dx = Array()
    dy = Array()
    safe_call(backend.get().af_sobel_operator(ct.pointer(dx.arr), ct.pointer(dy.arr),
                                              image.arr, ct.c_uint(w_len)))
    return dx,dy

def sobel_filter(image, w_len = 3, is_fast = False):
    """
    Apply sobel filter to the image.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image, or
          - A multi dimensional array representing batch of images.

    w_len : optional: int. default: 3.
          - The size of the sobel operator.

    is_fast : optional: bool. default: False.
          - Specifies if the magnitude is generated using SAD (if True) or SSD (if False).

    Returns
    ---------

    output : af.Array
           - Image containing the magnitude of the sobel derivatives.

    """
    from .arith import abs as af_abs
    from .arith import hypot as af_hypot

    dx,dy = sobel_derivatives(image, w_len)
    if (is_fast):
        return af_abs(dx) + af_abs(dy)
    else:
        return af_hypot(dx, dy)

def rgb2gray(image, r_factor = 0.2126, g_factor = 0.7152, b_factor = 0.0722):
    """
    Convert RGB image to Grayscale.

    Parameters
    ----------
    image : af.Array
          - A 3 D arrayfire array representing an 3 channel image, or
          - A multi dimensional array representing batch of images.

    r_factor : optional: scalar. default: 0.2126.
          - Weight for the red channel.

    g_factor : optional: scalar. default: 0.7152.
          - Weight for the green channel.

    b_factor : optional: scalar. default: 0.0722.
          - Weight for the blue channel.

    Returns
    --------

    output : af.Array
          - A grayscale image.

    """
    output=Array()
    safe_call(backend.get().af_rgb2gray(ct.pointer(output.arr),
                                        image.arr, ct.c_float(r_factor), ct.c_float(g_factor), ct.c_float(b_factor)))
    return output

def gray2rgb(image, r_factor = 1.0, g_factor = 1.0, b_factor = 1.0):
    """
    Convert Grayscale image to an RGB image.

    Parameters
    ----------
    image : af.Array
          - A 2 D arrayfire array representing an image, or
          - A multi dimensional array representing batch of images.

    r_factor : optional: scalar. default: 1.0.
          - Scale factor for the red channel.

    g_factor : optional: scalar. default: 1.0.
          - Scale factor for the green channel.

    b_factor : optional: scalar. default: 1.0
          - Scale factor for the blue channel.

    Returns
    --------

    output : af.Array
          - An RGB image.
          - The channels are not coalesced, i.e. they appear along the third dimension.

    """
    output=Array()
    safe_call(backend.get().af_gray2rgb(ct.pointer(output.arr),
                                        image.arr, ct.c_float(r_factor), ct.c_float(g_factor), ct.c_float(b_factor)))
    return output

def hsv2rgb(image):
    """
    Convert HSV image to RGB.

    Parameters
    ----------
    image : af.Array
          - A 3 D arrayfire array representing an 3 channel image, or
          - A multi dimensional array representing batch of images.

    Returns
    --------

    output : af.Array
          - A HSV image.

    """
    output = Array()
    safe_call(backend.get().af_hsv2rgb(ct.pointer(output.arr), image.arr))
    return output

def rgb2hsv(image):
    """
    Convert RGB image to HSV.

    Parameters
    ----------
    image : af.Array
          - A 3 D arrayfire array representing an 3 channel image, or
          - A multi dimensional array representing batch of images.

    Returns
    --------

    output : af.Array
          - A RGB image.

    """
    output = Array()
    safe_call(backend.get().af_rgb2hsv(ct.pointer(output.arr), image.arr))
    return output

def color_space(image, to_type, from_type):
    """
    Convert an image from one color space to another.

    Parameters
    ----------
    image : af.Array
          - A multi dimensional array representing batch of images in `from_type` color space.

    to_type : af.CSPACE
          - An enum for the destination color space.

    from_type : af.CSPACE
          - An enum for the source color space.

    Returns
    --------

    output : af.Array
          - An image in the `to_type` color space.

    """
    output = Array()
    safe_call(backend.get().af_color_space(ct.pointer(output.arr), image.arr,
                                           to_type.value, from_type.value))
    return output
