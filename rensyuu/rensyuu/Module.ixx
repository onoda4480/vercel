#include<stdio.h>
int main() {
    int h, w;
    int k = 1;
    while (1) {
        scanf_s("%d %d", &h, &w);
        if (h == 0 && w == 0)break;
        for (int i = 0; i < h; i++) {
            for (int x = 0; x < w; x++) {
                if (k == 1) {
                    printf("#");
                }
                else {
                    printf(".");
                }
                k *= -1;
            }
            if (w % 2 == 0) {
                k *= -1;
            }
            printf("\n");
        }
        printf("\n");
        k = 1;
    }
    return 0;
}
