#include <stdio.h>

// Este é apenas um simples comentario
int main (){
	char n[150];
	int cont = 0;
	scanf("%s", n);

	// another comentaruos
	for(int i=0; n[i]!= 0; i++){
		cont += n[i] -'0';
	}
	printf("%d", cont %3);
}
