#include <stdio.h>

/* VERSAO 1
int main (){
	unsigned long long n;
	scanf("%d", &n);
	
	while(n > 2){
		n -=3;
	}
	
	printf("%d", n);
} */

/* VERSAO 2
int main(){
	int n;
	scanf("%d", &n);
	printf("%d", n%3);
} */

/* infelizmente a versao final, pq n consigo representar um int gigante */

int main (){
	char n[150];
	int cont = 0;
	scanf("%s", n);
	
	for(int i=0; n[i]!= 0; i++){
		cont += n[i] -'0';
	}
	printf("%d", cont %3);
}
