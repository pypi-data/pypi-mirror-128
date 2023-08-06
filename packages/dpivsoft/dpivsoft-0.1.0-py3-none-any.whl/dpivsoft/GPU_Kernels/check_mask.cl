//Check if the point is inside the mask and set velocity to 0
//to prevent bleeding due to median filter

KERNEL void check_mask(GLOBAL_MEM float *uf,
GLOBAL_MEM float *vf,
GLOBAL_MEM int *x,
GLOBAL_MEM int *y,
GLOBAL_MEM bool *mask_img,
GLOBAL_MEM int *data)
{
    int width = data[0];

    int i = get_global_id(0);

    //Set velocity to 0 inside the mask
    int pos_mask = (y[i]) * width + x[i];

    if (mask_img[pos_mask]==0){
        uf[i] = 0;
        vf[i] = 0;
    }
}
