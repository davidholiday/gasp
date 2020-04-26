#include <iostream>
#include <string>
#include <cstdlib> // for EXIT_SUCCESS and EXIT_FAILURE
#include <boost/program_options.hpp>


int parse_program_options(int argc, char **argv) {
	namespace po = boost::program_options;
    po::options_description desc{"Allowed options"};

    
    desc.add_options()
        ("help,h", "display help message")
        ("floor", po::value<int>(), "floor of password size to generate")
        ("ceiling", po::value<int>(), "non-inclusive ceiling of password size to generate")
    ;
    
    po::positional_options_description floor_positional_option_description;
    floor_positional_option_description.add("floor", 0);
    
    po::positional_options_description ceiling_positional_option_description;
    ceiling_positional_option_description.add("ceiling", 1);
    
    po::command_line_parser parser{argc, argv};
    parser.options(desc).positional(floor_positional_option_description).allow_unregistered();
    parser.options(desc).positional(ceiling_positional_option_description).allow_unregistered();
    
    po::parsed_options parsed_options = parser.run();
    
    po::variables_map vm;
    po::store(parsed_options, vm);
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



