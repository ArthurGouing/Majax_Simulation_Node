__kernel void ker(__global float *a,
                  __global float *b,
                  __global float *c
                  )
{
    // Get thread id
    size_t thread_id = get_global_id(0);
    // Do the computation
    a[thread_id] = b[thread_id] + c[thread_id];
}