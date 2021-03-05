#include <stdio.h>
int sum(int a, int b)
{
	return a+b;
}
int sum2(int a, int b)
{
	return a+b;
}
int subtraction(int a,int b)
{
	return a-b;
}
int multipication(int a,int b)
{
	return a*b;
}
int main()
{
	int a=4;
	int b=2;
	int c=0;
	int d=2;
	b= 3*2;
	sum(a,b);
	sum2(a,c);
	subtraction(a,b);
	multipication(a,b);
	d=a&&b;
	d=a||b;
	d=a^b;
}
