#include <stdio.h>
#include <stdlib.h>
#include <math.h>

struct point {
    double x;
    double y;
    double z;
};

struct section {
    struct point P;
    struct point Q;
    struct point R;
    int num_points;
    struct point *points;
    double k;
};

void Generate_points(struct section *sect) {
    sect->points = malloc(sizeof(struct point) * sect->num_points);
    if (sect->points == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }
    
    double n1 = sect->R.x - sect->P.x;
    double n2 = sect->R.y - sect->P.y;
    double n3 = sect->R.z - sect->P.z;

    for (int i = 0; i < sect->num_points; i++) {
        double t = (double)i / (sect->num_points - 1);
        sect->points[i].x = n1 * t + sect->P.x;
        sect->points[i].y = n2 * t + sect->P.y;
        sect->points[i].z = n3 * t + sect->P.z;
    }
}

void Find_k(struct section *sect) {
    // Assuming that Q, R, and P are points and should be accessed directly
    double num_sum = (sect->Q.x - sect->R.x) * (sect->P.x - sect->Q.x) +
                     (sect->Q.y - sect->R.y) * (sect->P.y - sect->Q.y) +
                     (sect->Q.z - sect->R.z) * (sect->P.z - sect->Q.z);
    
    double dem_sum = (sect->Q.x - sect->R.x) * (sect->Q.x - sect->R.x) +
                     (sect->Q.y - sect->R.y) * (sect->Q.y - sect->R.y) +
                     (sect->Q.z - sect->R.z) * (sect->Q.z - sect->R.z);

    // Avoid division by zero
    if (dem_sum != 0) {
        sect->k = num_sum / dem_sum;
    } else {
        sect->k = 0; // Handle case where denominator is zero
    }
}

void free_points(struct section *sect) {
    free(sect->points);
    sect->points = NULL; // Prevent dangling pointer
}
