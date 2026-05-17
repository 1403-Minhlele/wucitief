#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
#define MAX 100  

void heapify(int *a, int k, int n) {
	int j = 2*k+1;
	while (j < n) {
			if (j + 1 < n) 
				if (a[j] < a[j + 1]) j = j + 1;
			if (a[k] >= a[j]) return;
			swap(a[k], a[j]); 	
			k = j; j = 2*k + 1;
	}
}
void buildHeap(int *a, int n) {
	int i;
	i = (n - 1) / 2;
	while (i >= 0) {
			heapify(a, i, n);
			i--;
	}
}
void heapSort(int *a, int n) {
	buildHeap(a, n);
	while (n > 0) {
			n = n - 1;
			swap(a[0], a[n]);
			heapify(a, 0, n);
	}
}


void Output(int A[], int N) {
    for (int i = 0; i < N; i++)
        cout<< A[i]<< " ";
           cout<<endl;
}

int main() {
    int A[]={12, 2, 18, 30, 5, 1, 6, 4, 15 };
    int N=9; 
    heapSort(A,N);
    Output(A,N);
    return 0;
}
 