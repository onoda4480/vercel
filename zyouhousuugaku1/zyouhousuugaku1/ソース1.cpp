#include <stdio.h>



int cnt = 0; //加算回数を格納する変数

int fibo(int n) {
	if (n == 0) return 0; //フィボナッチ数列の定義
	if (n == 1) return 1;
	if (n >= 2) {
		cnt++;
		return fibo(n - 1) + fibo(n - 2);
	}
}



int main(void) {
	int num;
	printf("第何項のフィボナッチ数Fnを求めますか？：");
	scanf_s("%d",&num);

	printf("第%d項のフィボナッチ数列は%dです。 ", num, fibo(num));
	printf("加算回数は%d回です。 ", cnt);
	return(0);
}