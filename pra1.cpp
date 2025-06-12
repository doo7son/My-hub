  #include <stdio.h>
  #include <stdlib.h>
  #include <malloc.h>

  int main(){

  int *fibo;
  int max, i;

  printf("피보나치 수열을 몇 번째까지 보시겠나요? ");
  scanf("%d", &max);

  if(max < 2){
    printf("2 이상의 자연수를 입력해 주세요.\n");
    
    exit(1);
  }

  fibo = (int*)malloc(max*sizeof(int));
  fibo[0] = 0;
  fibo[1] = 1;

  for(i=2; i<max; i++)
    fibo[i] = fibo[i-1] + fibo[i-2];

  for(i=0; i<max; i++)
    printf(" %d", fibo[i]);

  printf("\n");

  free(fibo);

  return 0;
  }