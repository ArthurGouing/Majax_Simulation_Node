__kernel void ker(
                  __global float *point, 
                  __global int *prim
                 )
{
    // Point id of the edge i
    int i = get_global_id(0);
    int id_1 = prim[2*i];
    int id_2 = prim[2*i+1];

    // Get points
    float3 p_1 = (float3)(point[id_1], point[id_1+1], point[id_1+2]);
    float3 p_2 = (float3)(point[id_2], point[id_2+1], point[id_2+2]);

    // Update points values
    point[3*id_1]   +=  0.01f;// new_p1[0];
    point[3*id_1+1] +=  0.01f;// new_p1[1];
    point[3*id_1+2] +=  0.01f;// new_p1[2];
    point[3*id_2]   +=  0.01f;// new_p2[0];
    point[3*id_2+1] +=  0.01f;// new_p2[1];
    point[3*id_2+2] +=  0.01f;// new_p2[2];
}