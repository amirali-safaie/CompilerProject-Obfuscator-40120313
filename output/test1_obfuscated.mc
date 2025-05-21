#include <stdio.h>
#include <stdbool.h>

int mf_0(int pm_0) {
    if (pm_0 <= 0) {
        return pm_0 + 2;
    }
    int temp_val = (pm_0 * 3) - (pm_0 / 5);
    return mf_0(pm_0 - 1) + (temp_val % 8);
}


int f_0(int p_0, int p_1) {
    int drv_0 = mf_0(2);
    int v_0 = p_0 + (0 - (p_1 / 5));
    return v_0;
}

int main() {
    int v_0 = 0;
    int v_1 = 0;
int v_2 = 0;
bool v_3 = true;
char v_4 = 's';
int v_5 = 2;
int st_2 = 1;
int dead_v_1 = 4580;
while (st_2 > 0) {
switch (st_2) {
case 1:
    for (v_0 = 0; v_0 < 5; v_0 = v_0 - (0 - (1)))    {
        int st_0 = 1;
        int drv_0 = mf_0(4);
        while (st_0 > 0) {
            switch (st_0) {
            case 1:
                v_1 = v_1 - (0 - (v_0));
                st_0 = 0;
                break;
            default:
                st_0 = 0;
                break;
        }
    }
}
    st_2 = 2;
    break;
case 2:
    printf("%d\n", v_1);
    st_2 = 3;
    break;
case 3:
    while (v_5 < 5){
    int st_1 = 1;
    int dead_v_0 = 6369;
    while (st_1 > 0) {
        switch (st_1) {
        case 1:
            v_2 = v_2 - (0 - (v_5));
            st_1 = 2;
            break;
        case 2:
            v_5 = v_5 - (0 - (1));
            st_1 = 0;
            break;
        default:
            st_1 = 0;
            break;
    }
}
}
    st_2 = 4;
    break;
case 4:
    printf("%d\n", v_2);
    st_2 = 5;
    break;
case 5:
    return 0;
    st_2 = 0;
    break;
default:
    st_2 = 0;
    break;
}
}
}