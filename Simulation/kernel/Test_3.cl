__kernel void ker(__global float *a, float dt)
{
    int id = get_global_id(0);
    a[id] = a[id] + dt;
}