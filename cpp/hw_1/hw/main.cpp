#include <iostream>
#include <string>
#include <cstdlib> // for EXIT_SUCCESS and EXIT_FAILURE
#include <boost/program_options.hpp>


int parse_program_options(int argc, char **argv) {
	namespace po = boost::program_options;
    
    int floor;
    int ceiling;
    
    po::options_description desc{"Allowed options"};    
    desc.add_options()
        ("help,h", "display help message")
//        ("floor", po::value<int>(), "floor of password size to generate")
//        ("ceiling", po::value<int>(), "non-inclusive ceiling of password size to generate")
    ;
    
    po::options_description hidden_desc;
    hidden_desc.add_options()
        ("floor", po::value<int>(&floor)->required(), "floor of password size to generate")
        ("ceiling", po::value<int>(&ceiling)->required(), "non-inclusive ceiling of password size to generate")
    ;

    po::options_description all_desc;
    all_desc.add(desc);
    all_desc.add(hidden_desc);
    
    po::positional_options_description positional_desc;
    positional_desc.add("floor", 1);
    positional_desc.add("ceiling", 2);
    
    po::variables_map vm;
    
    po::parsed_options parsed = 
        po::command_line_parser(argc, argv).options(all_desc)
                                           .positional(positional_desc)
                                           .run();
    po::store(parsed, vm);
    po::notify(vm);
    
    if (vm.count("help")) {
        std::cout << desc << '\n';
    }
    
    
    
	return EXIT_SUCCESS;
}


int main(int argc, char **argv) {
    int parse_program_options_rc = parse_program_options(argc, argv);
    return parse_program_options_rc;
}



