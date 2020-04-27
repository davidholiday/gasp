#include <iostream>
#include <string>
#include <cstdlib> // for EXIT_SUCCESS and EXIT_FAILURE
#include <boost/program_options.hpp>


int parse_program_options(int argc, char **argv) {

    namespace po = boost::program_options;
    
    std::string desc_txt = "Description:\n"
                           "generates all possible combinations of printable characters, rates them with zxcvbn, and "
                           "serializes by length and rating.";
    
    // for holding onto positional argument values 
    int floor_value;
    int ceiling_value;

    
    // named argument descriptions
    po::options_description desc{"Allowed options"};    
    desc.add_options()
        ("help,h", "display help message") 
        ("floor,f", po::value<int>(&floor_value), "(required) floor of password size to generate")
        ("ceiling,c", po::value<int>(&ceiling_value), "(required) non-inclusive ceiling of password size to generate")
    ;

    
    // parse caller input
    po::variables_map vm;
    
    try {
        
        po::command_line_parser parser = po::command_line_parser(argc, argv).options(desc);
        po::parsed_options parsed = parser.run();
        po::store(parsed, vm);
        po::notify(vm);
        
        if (vm.count("help")) {
            std::cout << desc_txt << "\n\n";
            std::cout << desc << "\n";
        }      

        if ( !(vm.count("floor") && vm.count("ceiling")) ) {
            throw std::invalid_argument("both floor and ceiling parameters must be specified");
        }


 
    } catch (std::exception &ex) {
        std::cerr << ex.what() << "\n\n";
        std::cout << desc_txt << "\n\n";
        std::cout << desc << "\n";
    }


	return EXIT_SUCCESS;
}






int main(int argc, char **argv) {
    int parse_program_options_rc = parse_program_options(argc, argv);
    return parse_program_options_rc;
}



