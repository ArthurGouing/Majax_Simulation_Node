// ALIAS a = geometry_buffers_points_out
//@ALIAS@ geometry_buffers_pt_var_masse_in @ b
//@alias@ my_personal_name_pt_var_accel_in@c

__kernel void ker(__global float *a,
                  __global float *b,
                  __global float *c
                  )
{
    // Get thread id
    size_t thread_id = get_global_id(0);
    // Do the computation
    a[thread_id] = b[thread_id] * c[thread_id];
}