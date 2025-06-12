#include <stdio.h>
#include <stdlib.h>
#define MAX 20
int goal[3][3]={
    1,2,3,
    4,0,5,
    6,7,8
};
int open[MAX];
int close[MAX];

typedef struct node
{
    int a[3][3];
    int k;  //평가함수 값값
    int blank;//빈칸의 위치치
    struct node* link;

}node;

//자식 생성 함수 필요

int find_blank(node* p)
{
    int count=0;
    for(int i=0; i<3; i++)
    {
        for(int j=0; j<3; j++)
        {
            count++;
            if(p->a[i][j]==0)
            {
                return count-1;
            }
        }
    }
}


//평가함수 값 리턴 함수 필요
int h(struct node* node)
{   
    int count=0;
    for(int i=0; i<3; i++)
    {
        for(int j=0; j<3; j++)
        {
            if(node->a[i][j]==goal[i][j])
            {
                count++;
                if(count==8)
                {
                    printf("find!\n");
                    return 0;
                }


            }

        }

    }
    return count;
    
}



node* crate_node(struct node* p)
{
    node* new_node=(node*)malloc(sizeof(node));
    if(!new_node)
    {
        printf("error!\n");
    }

    for(int i=0; i<3; i++)
    {
        for(int j=0; j<3; j++)
        {
            new_node->a[i][j]=p->a[i][j];
        }
        
    }
    new_node->blank=find_blank(new_node);
    new_node->k=h(new_node);
    new_node->link=NULL;

    return new_node;

}

void sort(int open[])// open 정렬
{
    int temp, j;

    for(int i=0; i<MAX; i++)
    {
        for(j=i+1; j<MAX; j++)
        {
            if(open[i]>open[j])
            {
                temp=open[i];
                open[i]=open[j];
                open[j]=temp;
            }
        }
        
        
    }

}




int main(void)
{

    int A[MAX]={3,1,2,4};

    sort(A);
    for(int i=0; i<MAX; i++)
    {
        printf("%3d", A[i]);
    }


    return 0;
}