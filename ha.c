#include <stdio.h>

// 하노이탑 재귀 함수
void hanoi(int n, int from, int by, int to) {
    // 기본 케이스: 원반이 1개일 경우
    if (n == 1) {
        printf("%d에서 %d로 원반을 옮깁니다.\n", from, to);
        return;
    }
    
    // 1. n-1개의 원반을 from에서 by로 옮깁니다. (to를 보조로 사용)
    hanoi(n - 1, from, to, by);
    
    // 2. 가장 큰 원반(n)을 from에서 to로 옮깁니다.
    printf("%d에서 %d로 원반을 옮깁니다.\n", from, to);
    
    // 3. n-1개의 원반을 by에서 to로 옮깁니다. (from을 보조로 사용)
    hanoi(n - 1, by, from, to);
}

int main() {
    int num_disks = 3; // 원반 개수
    
    // 하노이탑 함수 호출 (1번 기둥에서 3번 기둥으로, 2번 기둥을 보조로 사용)
    hanoi(num_disks, 1, 2, 3);
    
    return 0;
}

