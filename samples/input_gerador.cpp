#include <stdio.h>

main() {
 int n, k, f1,f2, f3;

	scanf('%d', &n);
	f1=0; f2=1; k=1;
	while (k<= n )
	{
		f3 =f1+f2;
		f1 =f2;
		f2 =f3;
		k =k+1;
	}
	printf ('%d %d',n, f1);
}