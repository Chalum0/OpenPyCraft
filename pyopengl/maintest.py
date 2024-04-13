import numpy as np
import pyopencl as cl
import time


def add_arrays_python(a, b):
    result = a.copy()  # Start with a copy of a to avoid modifying the original array
    for _ in range(500):
        result = result + b
    return result


def add_arrays_opencl(a_np, b_np):
    platform = cl.get_platforms()[0]
    device = platform.get_devices()[0]
    context = cl.Context([device])
    queue = cl.CommandQueue(context)

    a_buf = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=a_np)
    b_buf = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=b_np)
    result_buf = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, a_np.nbytes)
    kernel_code = """
    __kernel void add_arrays(__global const float* a, __global const float* b, __global float* result) {
    int id = get_global_id(0);
    float temp = a[id];
    for (int i = 0; i < 500; i++) {
        temp += b[id];
    }
    result[id] = temp;
}
    """
    program = cl.Program(context, kernel_code).build()
    program.add_arrays(queue, a_np.shape, None, a_buf, b_buf, result_buf)
    result_np = np.empty_like(a_np)
    cl.enqueue_copy(queue, result_np, result_buf)
    return result_np


# Generate two large arrays
a_np = np.random.rand(1000000).astype(np.float32)
b_np = np.random.rand(1000000).astype(np.float32)

# Time the Python function
start_time = time.time()
result_python = add_arrays_python(a_np, b_np)
python_time = time.time() - start_time

# Time the OpenCL function
start_time = time.time()
result_opencl = add_arrays_opencl(a_np, b_np)
opencl_time = time.time() - start_time

print(f"Python time: {python_time:.5f} seconds")
print(f"OpenCL time: {opencl_time:.5f} seconds")

# You can also check if the results are similar to ensure correctness
assert np.allclose(result_python, result_opencl), "Results differ between Python and OpenCL implementations!"
