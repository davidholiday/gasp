#include <iostream>
#include <string>
#include <cstdlib> // for EXIT_SUCCESS and EXIT_FAILURE
#include <boost/program_options.hpp>


#define OUT


int parse_program_options(int argc, char **argv, OUT int& floorOut, OUT int& ceilingOut) {

    int rc = EXIT_SUCCESS;
    namespace po = boost::program_options;
    
    std::string desc_txt = "Description:\n"
                           "generates all possible combinations of printable characters, rates them with zxcvbn, and "
                           "serializes by length and rating.";
        
    // named argument descriptions
    po::options_description desc{"Allowed options"};    
    desc.add_options()
        ("help,h", "display help message") 
        ("floor,f", po::value<int>(&floorOut), "(required) floor of password size to generate")
        ("ceiling,c", po::value<int>(&ceilingOut), "(required) non-inclusive ceiling of password size to generate")
    ;

    
    // parse caller input
    po::variables_map vm;
    
    try {
        
        po::command_line_parser parser = po::command_line_parser(argc, argv).options(desc);
        po::parsed_options parsed = parser.run();
        po::store(parsed, vm);
        po::notify(vm);
        
        
        // validation 
        if ( !vm.count("floor") || !vm.count("ceiling") ) {
            throw std::invalid_argument("both floor and ceiling parameters must be specified");
        }

        if (floorOut < 1) {
            throw std::invalid_argument("floor must be greater than 0 ");
        }
        
        if (ceilingOut <= floorOut) {
            throw std::invalid_argument("ceiling value must be greater than floor value");
        }
        
        
        // respond
        if (vm.count("help")) {
            std::cout << desc_txt << "\n\n";
            std::cout << desc << "\n";
        }      

    } catch (std::exception &ex) {
        std::cerr << ex.what() << "\n\n";
        std::cout << desc_txt << "\n\n";
        std::cout << desc << "\n";
        rc = EXIT_FAILURE;
    }


	return rc;
}






int main(int argc, char **argv) {
    int rc = EXIT_SUCCESS;
    
    int floor, ceiling;
    int parse_program_options_rc = parse_program_options(argc, argv, floor, ceiling);
    
    if (parse_program_options_rc == EXIT_FAILURE) {
        rc = EXIT_FAILURE;
    } else {
        std::cout << "floor value is: " << floor << "   ceiling value is: " << ceiling << "\n";
    }
    
    return rc;
}



