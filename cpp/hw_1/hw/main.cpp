//#include <stdio.h>
//#include <cstdlib> // for EXIT_SUCCESS and EXIT_FAILURE
//
//int main(int argc, char **argv)
//{
//	printf("hello world\n");
//	return EXIT_SUCCESS;
//}
#include <iostream>
#include <boost/array.hpp>

using namespace std;
int main(){
  boost::array<int, 4> arr = {{1,2,3,4}};
  cout << "hi" << arr[0];
  return 0;
}