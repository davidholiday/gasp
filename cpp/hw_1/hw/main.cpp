#include <stdio.h>
#include <cstdlib> // for EXIT_SUCCESS and EXIT_FAILURE
#include <boost/program_options.hpp>

int main(int argc, char **argv) {
	namespace po = boost::program_options;
    po::options_description desc{"Allowed options"};
    desc.add_options()
        ("help", "display help message")
        ("floor", po::value<int>(), "floor of password size to generate")
        ("ceiling", po::value<int>(), "non-inclusive ceiling of password size to generate")
    ;
    
	return EXIT_SUCCESS;
}

