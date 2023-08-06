import time
import cv2
import numpy as np
import importlib_resources

import reikna.cluda as cluda
import reikna.cluda.dtypes as dtypes
from reikna.core import Transformation, Parameter, Annotation, Type
from reikna.cluda import functions, dtypes
from reikna.fft import FFT, FFTShift
from reikna.cluda.tempalloc import ZeroOffsetManager

import dpivsoft.DPIV as DPIV      #Python PIV implementation
from dpivsoft.Classes  import Parameters
from dpivsoft.Classes  import grid
from dpivsoft.Classes  import GPU

def select_Platform(idx):
    """
    Selection of the device to run opencl calculations.

    idx: identifier int of platform in the computer.

    if idx is a string called "selection", the terminal shows a list
    of all available platforms in the computer to select one.
    """

    dtype = np.complex64
    api = cluda.ocl_api()
    if idx is "selection":
        thr = api.Thread.create(interactive=True)
    else:
        thr = api.Thread.create(idx)

    return thr

def compile_Kernels(thr):
    """
    Compiles all kernels needed for GPU calculation.
    Only needs to be called once.

    Kernels are by default in relative the path: ./GPU_Kernels.
    """

    # Package instalation path
    path = importlib_resources.files("dpivsoft")

    # Split image Kernel
    program = thr.compile(open(path/"GPU_Kernels/Slice.cl").read())
    GPU.Slice = program.Slice

    # Normalize image Kernel
    program = thr.compile(open(path/"GPU_Kernels/SubMean.cl").read())
    GPU.SubMean = program.SubMean

    program = thr.compile(open(path/"GPU_Kernels/Normalize_Img.cl").read())
    GPU.Normalize = program.Normalize

    # Multiplication Kernel
    program = thr.compile(open(path/"GPU_Kernels/multiply_them.cl").read(),
        render_kwds=dict(ctype1=dtypes.ctype(np.complex64),
        ctype2=dtypes.ctype(np.complex64),
        mul=functions.mul(np.complex64, np.complex64)))
    GPU.multiply_them = program.multiply_them

    # Apply mask Kernel
    program = thr.compile(open(path/"GPU_Kernels/multiply_them.cl").read(),
        render_kwds = dict(ctype1=dtypes.ctype(np.float32),
        ctype2 = dtypes.ctype(bool),
        mul = functions.mul(np.float32, bool)))
    GPU.masking = program.multiply_them

    # Find Maximun Kernel
    program = thr.compile(open(path/"GPU_Kernels/find_peak.cl").read())
    GPU.find_peak = program.find_peak

    # Interpolation Kernel
    program = thr.compile(open(path/"GPU_Kernels/interpolation.cl").read())
    GPU.interpolate = program.Interpolation

    # Jacobian Kernel
    program = thr.compile(open(path/"GPU_Kernels/Jacobian.cl").read())
    GPU.jacobian = program.Jacobian

    # Box blur filter
    program = thr.compile(open(path/"GPU_Kernels/box_blur.cl").read())
    GPU.box_blur = program.box_blur

    # Deform image kernel
    program = thr.compile(open(path/"GPU_Kernels/deform_image.cl").read())
    GPU.deform_image = program.Deform_image

    # Median Filter
    program = thr.compile(open(path/"GPU_Kernels/median_filter.cl").read())
    GPU.Median_Filter = program.Median_Filter

    # Check if inside mask
    program = thr.compile(open(path/"GPU_Kernels/check_mask.cl").read())
    GPU.check_mask = program.check_mask

    # Weighting function
    program = thr.compile(open(path/"GPU_Kernels/Weighting.cl").read())
    GPU.Weighting = program.Weighting

    thr.synchronize()

def initialization(width, height, thr):
    """
    Initialize variables in GPU memory
    """

    # Obtain PIV mesh
    grid.generate_mesh(width,height)
    grid.pixels = width*height

    # Total number of boxes for global size
    N_boxes_1 = Parameters.no_boxes_1_x*Parameters.no_boxes_1_y
    N_boxes_2 = Parameters.no_boxes_2_x*Parameters.no_boxes_2_y

    # Initialice velocity vectors solution fot first step
    u1 = np.zeros([Parameters.no_boxes_1_y,
        Parameters.no_boxes_1_x]).astype(np.float32)
    v1 = np.zeros([Parameters.no_boxes_1_y,
        Parameters.no_boxes_1_x]).astype(np.float32)

    # Initialize Subimage matrix
    subImg1 = np.zeros((N_boxes_1, Parameters.box_size_1_y,
        Parameters.box_size_1_x), dtype = np.complex64)
    subImg2 = np.zeros((N_boxes_2, Parameters.box_size_2_y,
        Parameters.box_size_2_x), dtype = np.complex64)
    frac1 = np.zeros((N_boxes_1, Parameters.box_size_1_y,
        Parameters.box_size_1_x), dtype = np.float32)
    frac = np.zeros((N_boxes_2, Parameters.box_size_2_y,
        Parameters.box_size_2_x), dtype = np.float32)
    subMean1 = np.zeros((Parameters.no_boxes_1_y, Parameters.no_boxes_1_x),
        dtype = np.float32)
    subMean2 = np.zeros((Parameters.no_boxes_2_y, Parameters.no_boxes_2_x),
        dtype = np.float32)

    # Array of parameters data
    peak_ratio = int(Parameters.peak_ratio*1000)  #trick pass this value as int

    data1 = np.array((width, height,
        Parameters.box_size_1_x, Parameters.box_size_1_y,
        Parameters.no_boxes_1_x, Parameters.no_boxes_1_y,
        Parameters.window_x_1, Parameters.window_y_1,
        peak_ratio)).astype(np.int32)
    data2 = np.array((width, height,
        Parameters.box_size_2_x, Parameters.box_size_2_y,
        Parameters.no_boxes_2_x, Parameters.no_boxes_2_y,
        Parameters.window_x_2, Parameters.window_y_2,
        peak_ratio)).astype(np.int32)

    # Initialice velocity vectors solution fot first step
    u1 = np.zeros([Parameters.no_boxes_1_y,
        Parameters.no_boxes_1_x]).astype(np.float32)
    v1 = np.zeros([Parameters.no_boxes_1_y,
        Parameters.no_boxes_1_x]).astype(np.float32)

    # Initialice velocity vectors solution for second step
    u2 = np.zeros([Parameters.no_boxes_2_y,
        Parameters.no_boxes_2_x]).astype(np.float32)
    v2 = np.zeros([Parameters.no_boxes_2_y,
        Parameters.no_boxes_2_x]).astype(np.float32)

    # Send mesh to gpu (only done once)
    GPU.box_origin_x_1 = thr.to_device(grid.box_origin_x_1)
    GPU.box_origin_y_1 = thr.to_device(grid.box_origin_y_1)
    GPU.box_origin_x_2 = thr.to_device(grid.box_origin_x_2)
    GPU.box_origin_y_2 = thr.to_device(grid.box_origin_y_2)

    GPU.x1 = thr.to_device(grid.x_1)
    GPU.y1 = thr.to_device(grid.y_1)
    GPU.x2 = thr.to_device(grid.x_2)
    GPU.y2 = thr.to_device(grid.y_2)

    # Send PIV parameters to gpu (only done once)
    GPU.data1 = thr.to_device(data1)
    GPU.data2 = thr.to_device(data2)
    GPU.median_limit = thr.to_device(np.float32(Parameters.median_limit))


    # Initialice all intermediate variables on gpu (only done one)
    GPU.subImg1_1 = thr.empty_like(subImg1)
    GPU.subImg1_2 = thr.empty_like(subImg1)

    GPU.subImg2_1 = thr.empty_like(subImg2)
    GPU.subImg2_2 = thr.empty_like(subImg2)

    """
    #Subimages complety managed with temp_manager to save memory.
    #Currently is not working due to Reikna Package bug. If you are
    #interested on using it, clone and install the tempalloc-fix
    #branch of Reikna package in git. This fix is not yet upload to pypi.
    #For using the temp_manager, delete or comment the previous
    #initialization of GPU images and uncomment this implementation

    #Temp manager
    temp_manager = ZeroOffsetManager(
            thr, pack_on_alloc=True, pack_on_free=True)

    GPU.subImg1_1 = temp_manager.array([N_boxes_1,
        Parameters.box_size_1_y, Parameters.box_size_1_x],
        np.complex64)
    GPU.subImg1_2 = temp_manager.array([N_boxes_1,
        Parameters.box_size_1_y, Parameters.box_size_1_x],
        np.complex64, dependencies = [GPU.subImg1_1])

    GPU.subImg2_1 = temp_manager.array([N_boxes_2,
        Parameters.box_size_2_y, Parameters.box_size_2_x],
        np.complex64)
    GPU.subImg2_2 = temp_manager.array([N_boxes_2,
        Parameters.box_size_2_y, Parameters.box_size_2_x],
        np.complex64, dependencies = [GPU.subImg2_1])
    """

    GPU.u_index_1 = thr.to_device(frac1)
    GPU.v_index_1 = thr.to_device(frac1)
    GPU.u_index_2 = thr.to_device(frac)
    GPU.v_index_2 = thr.to_device(frac)

    GPU.subMean1_1 = thr.to_device(subMean1)
    GPU.subMean1_2 = thr.to_device(subMean1)
    GPU.subMean2_1 = thr.to_device(subMean2)
    GPU.subMean2_2 = thr.to_device(subMean2)

    GPU.u1 = thr.empty_like(u1)
    GPU.v1 = thr.empty_like(v1)
    GPU.u1_f = thr.empty_like(u1)
    GPU.v1_f = thr.empty_like(v1)
    GPU.u2 = thr.empty_like(u2)
    GPU.v2 = thr.empty_like(u2)
    GPU.u2_f = thr.empty_like(u2)
    GPU.v2_f = thr.empty_like(u2)

    GPU.du_dx_1 = thr.empty_like(u1)
    GPU.du_dy_1 = thr.empty_like(u1)
    GPU.dv_dx_1 = thr.empty_like(u1)
    GPU.dv_dy_1 = thr.empty_like(u1)
    GPU.temp_dx = thr.empty_like(u1)
    GPU.temp_dy = thr.empty_like(u1)
    GPU.temp_dx_2 = thr.empty_like(u2)
    GPU.temp_dy_2 = thr.empty_like(u2)

    GPU.du_dx_2 = thr.empty_like(u2)
    GPU.du_dy_2 = thr.empty_like(u2)
    GPU.dv_dx_2 = thr.empty_like(u2)
    GPU.dv_dy_2 = thr.empty_like(u2)

    # Load mask if any
    if Parameters.mask:
        GPU.mask = thr.to_device(Parameters.Data.mask)
    else:
        temp = np.zeros(2);
        GPU.mask = thr.empty_like(temp)

    # Initialize GPU computations for the cross-correlation
    GPU.axes = (1,2)
    GPU.fft = FFT(subImg1, axes=GPU.axes).compile(thr)
    GPU.fftshift = FFTShift(subImg1, axes=GPU.axes).compile(thr)

    GPU.fft2 = FFT(subImg2, axes=GPU.axes).compile(thr)
    GPU.fftshift2 = FFTShift(subImg2, axes=GPU.axes).compile(thr)


def processing(img1_name, img2_name, thr):
    """
    Perform a parallelized 2 pass PIV algorithm with window deformation
    executed on openCL.

    Developed by Jorge Aguilar-Cabello

    Inputs:
    -------
    Img1: 2d array of simple float
        Image from a flow field with trazers particles inside it.

    Img2: 2d array of simple float
        Image consecutive to Img1.

    thr: openCL object
        Platform where to perform the operations in openCL.

    Parameters: class
        Saved in  "Classes.py" file. It contains all PIV procesing parameters
        to be used in calculations. Parameters can be changed manually or
        loaded from external file by using the classmethod: "readParameters".
        Use $help class for more information about PIV parameters.

    Outputs:
    --------
    GPU: Class
        Saved in "Classes.py". Containing all data stored in GPU memory.
        Following outputs are all included inside this class.

    gx1: GPU 2d array
        x meshgrid on GPU from first sweep.

    gx2: GPU 2d array
        x meshgrid on GPU from second sweep.

    gy1: GPU 2d array
        y meshgrid on GPU from first sweep.

    gy2: GPU 2d array
        y meshgrid on GPU from second sweep.

    gu1: GPU 2d array
        velocity field in x direction on GPU from first sweep

    gu2: GPU 2d array
        velocity field in x direction on GPU from second sweep

    gv1: GPU 2d array
        velocity field in y direction on GPU from first sweep

    gv2: GPU 2d array
        velocity field in y direction on GPU from second sweep
    """

    N_boxes_1 = Parameters.no_boxes_1_x*Parameters.no_boxes_1_y
    N_boxes_2 = Parameters.no_boxes_2_x*Parameters.no_boxes_2_y
    N_pixels_1 = N_boxes_1*Parameters.box_size_1_x*Parameters.box_size_1_y
    N_pixels_2 = N_boxes_2*Parameters.box_size_2_x*Parameters.box_size_2_y

    # Image Gaussian filter if required
    if Parameters.gaussian_filter:
        # Reserved to implement the filter
        pass

    # Mask images if required
    if Parameters.mask:
        # Reserved to implement the mask
        GPU.masking(GPU.img1, GPU.img1, GPU.mask, local_size=None,
                global_size = grid.pixels)
        GPU.masking(GPU.img2, GPU.img2, GPU.mask, local_size=None,
                global_size = grid.pixels)

    # Obtain SubImage
    GPU.Slice(GPU.subImg1_1, GPU.img1, GPU.box_origin_x_1, GPU.box_origin_y_1,
            GPU.data1, local_size = None, global_size = N_pixels_1)
    GPU.Slice(GPU.subImg1_2, GPU.img2, GPU.box_origin_x_1, GPU.box_origin_y_1,
            GPU.data1, local_size = None, global_size = N_pixels_1)

    for i in range(0,Parameters.no_iter_1):
        if i:
            # Median Filter
            GPU.Median_Filter(GPU.u1_f, GPU.v1_f, GPU.u1, GPU.v1,
                    GPU.median_limit, GPU.data1, local_size = None,
                    global_size = N_boxes_1)

            # Velocity=0 inside mask to prevent bleeding from median filter
            if Parameters.mask:
                GPU.check_mask(GPU.u1_f, GPU.v1_f, GPU.x1, GPU.y1,
                        GPU.mask, GPU.data1, local_size = None,
                        global_size = N_boxes_1)

            # Jacobian matrix
            GPU.jacobian(GPU.temp_dx, GPU.temp_dy, GPU.u1_f, GPU.x1, GPU.y1,
                    GPU.data1, local_size = None, global_size = N_boxes_1)
            GPU.box_blur(GPU.du_dx_1, GPU.temp_dx, GPU.data1,
                    local_size = None, global_size = N_boxes_1)
            GPU.box_blur(GPU.du_dy_1, GPU.temp_dy, GPU.data1,
                    local_size = None, global_size = N_boxes_1)

            GPU.jacobian(GPU.temp_dx, GPU.temp_dy, GPU.v1_f, GPU.x1, GPU.y1,
                    GPU.data1, local_size = None, global_size = N_boxes_1)
            GPU.box_blur(GPU.dv_dx_1, GPU.temp_dx, GPU.data1,
                    local_size = None, global_size = N_boxes_1)
            GPU.box_blur(GPU.dv_dy_1, GPU.temp_dy, GPU.data1,
                    local_size = None, global_size = N_boxes_1)

            # Deformed image
            GPU.deform_image(GPU.subImg1_1, GPU.subImg1_2, GPU.img1, GPU.img2,
                    GPU.box_origin_x_1, GPU.box_origin_y_1, GPU.u1_f,
                    GPU.v1_f, GPU.du_dx_1, GPU.du_dy_1, GPU.dv_dx_1,
                    GPU.dv_dy_1, GPU.u_index_1, GPU.v_index_1, GPU.data1,
                    local_size = None, global_size = N_pixels_1)

        # Normalize
        GPU.SubMean(GPU.subMean1_1, GPU.subImg1_1, GPU.data1,
                local_size = None, global_size = N_boxes_1)
        GPU.SubMean(GPU.subMean1_2, GPU.subImg1_2, GPU.data1,
                local_size = None, global_size = N_boxes_1)

        GPU.Normalize(GPU.subImg1_1, GPU.subMean1_1, GPU.data1,
                local_size = None, global_size = N_pixels_1)
        GPU.Normalize(GPU.subImg1_2, GPU.subMean1_2, GPU.data1,
                local_size = None, global_size = N_pixels_1)

        # Weighting if required
        if Parameters.weighting:
            GPU.Weighting(GPU.subImg1_1, GPU.data1, local_size = None,
                    global_size = N_pixels_1)
            GPU.Weighting(GPU.subImg1_2, GPU.data1, local_size = None,
                    global_size = N_pixels_1)

        # FFT2D
        GPU.fft(GPU.subImg1_1, GPU.subImg1_1)
        GPU.fft(GPU.subImg1_2, GPU.subImg1_2)

        # Conjugate
        GPU.subImg1_1 = GPU.subImg1_1.conj()

        # Multiplication
        GPU.multiply_them(GPU.subImg1_1, GPU.subImg1_1, GPU.subImg1_2,
                local_size = None, global_size = N_pixels_1)

        # Inverse transform
        GPU.fft(GPU.subImg1_1, GPU.subImg1_1, inverse=True)

        # FFTShift
        GPU.fftshift(GPU.subImg1_1, GPU.subImg1_1)

        # Find peak
        GPU.find_peak(GPU.v1, GPU.u1, GPU.subImg1_1, GPU.u_index_1,
                GPU.v_index_1, GPU.data1, local_size = None,
                global_size = N_boxes_1)

    # Interpolate velocity results from first mesh
    GPU.interpolate(GPU.u2_f, GPU.u1, GPU.x2, GPU.y2, GPU.x1, GPU.y1,
            GPU.data1, local_size = None, global_size = N_boxes_2)
    GPU.interpolate(GPU.v2_f, GPU.v1, GPU.x2, GPU.y2, GPU.x1, GPU.y1,
            GPU.data1, local_size = None, global_size = N_boxes_2)


    for i in range(0,Parameters.no_iter_2):

        # Jacobian matrix
        GPU.jacobian(GPU.temp_dx_2, GPU.temp_dy_2, GPU.u2_f, GPU.x2, GPU.y2,
                GPU.data2, local_size = None, global_size = N_boxes_2)
        GPU.box_blur(GPU.du_dx_2, GPU.temp_dx_2, GPU.data2, local_size = None,
                global_size = N_boxes_2)
        GPU.box_blur(GPU.du_dy_2, GPU.temp_dy_2, GPU.data2, local_size = None,
                global_size = N_boxes_2)

        GPU.jacobian(GPU.temp_dx_2, GPU.temp_dy_2, GPU.v2_f, GPU.x2, GPU.y2,
                GPU.data2, local_size = None, global_size = N_boxes_2)
        GPU.box_blur(GPU.dv_dx_2, GPU.temp_dx_2, GPU.data2, local_size = None,
                global_size = N_boxes_2)
        GPU.box_blur(GPU.dv_dy_2, GPU.temp_dy_2, GPU.data2, local_size = None,
                global_size = N_boxes_2)

        # Deformed image
        GPU.deform_image(GPU.subImg2_1, GPU.subImg2_2, GPU.img1, GPU.img2,
                GPU.box_origin_x_2, GPU.box_origin_y_2, GPU.u2_f,
                GPU.v2_f, GPU.du_dx_2, GPU.du_dy_2, GPU.dv_dx_2,
                GPU.dv_dy_2, GPU.u_index_2, GPU.v_index_2, GPU.data2,
                local_size = None, global_size = N_pixels_2)

        # Normalize
        GPU.SubMean(GPU.subMean2_1,GPU.subImg2_1,GPU.data2,
               local_size = None, global_size = N_boxes_2)
        GPU.SubMean(GPU.subMean2_2,GPU.subImg2_2,GPU.data2,
                local_size = None, global_size = N_boxes_2)

        GPU.Normalize(GPU.subImg2_1,GPU.subMean2_1,GPU.data2,
                local_size = None, global_size = N_pixels_2)
        GPU.Normalize(GPU.subImg2_2,GPU.subMean2_2,GPU.data2,
                local_size = None, global_size = N_pixels_2)

        # Weighting if required
        if Parameters.weighting:
            GPU.Weighting(GPU.subImg2_1, GPU.data2, local_size = None,
                    global_size = N_pixels_2)
            GPU.Weighting(GPU.subImg2_2, GPU.data2, local_size = None,
                    global_size = N_pixels_2)

        # FFT2D
        GPU.fft2(GPU.subImg2_1, GPU.subImg2_1)
        GPU.fft2(GPU.subImg2_2, GPU.subImg2_2)

        # Conjugate
        GPU.subImg2_1 = GPU.subImg2_1.conj()

        # Multiplication
        GPU.multiply_them(GPU.subImg2_1, GPU.subImg2_1, GPU.subImg2_2,
                local_size=None, global_size = N_pixels_2)

        # Inverse transform
        GPU.fft2(GPU.subImg2_1, GPU.subImg2_1, inverse=True)

        # FFTShift
        GPU.fftshift2(GPU.subImg2_1, GPU.subImg2_1)

        # Find peak
        GPU.find_peak(GPU.v2, GPU.u2, GPU.subImg2_1, GPU.u_index_2,
                GPU.v_index_2, GPU.data2, local_size = None,
                global_size = N_boxes_2)

        # Median Filter
        GPU.Median_Filter(GPU.u2_f, GPU.v2_f, GPU.u2, GPU.v2,
                GPU.median_limit, GPU.data2, local_size = None,
                global_size = N_boxes_2)

        if Parameters.mask:
            # Check if inside mask to prevent bleeding from median filter
            GPU.check_mask(GPU.u2_f, GPU.v2_f, GPU.x2, GPU.y2,
                    GPU.mask, GPU.data2, local_size = None,
                    global_size = N_boxes_2)


    # Load Images of next iteration during runtime
    Img1, Img2 = DPIV.load_images(img1_name, img2_name)

    thr.synchronize()

    #Send next iteration images to the GPU
    GPU.img1 = thr.to_device(Img1)
    GPU.img2 = thr.to_device(Img2)

    return 1
