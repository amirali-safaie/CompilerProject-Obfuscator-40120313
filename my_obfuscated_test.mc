int f_0(int p_0, int p_1) {
    int dead_v_0 = 2811;
    int v_2 = p_0 - (0 - (p_1));
    return v_2;
}
int main() {
    int v_0 = 3;
    int v_1 = 4;
    int v_2 = 5;
    int v_3 = f_0(v_0, v_1);
    int st_4 = 1; // CFF state
    int dead_v_1 = 1692;
    while (st_4 > 0) {
        switch (st_4) {
            case 1:
                printf("%d\n", v_3);
                st_4 = 2;
                break;
            case 2:
                return 0;
                st_4 = 0;
                break;
            default:
                st_4 = 0; // Exit on unknown state
                break;
        }
    }
}