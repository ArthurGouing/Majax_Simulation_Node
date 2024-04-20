__kernel void ker(__global float *a)
{
    int id = get_global_id(0);
    a[id] = a[id] + 0.01f;
}