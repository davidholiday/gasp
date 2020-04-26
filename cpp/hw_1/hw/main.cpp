#include <iostream>
#include <string>
#include <cstdlib> // for EXIT_SUCCESS and EXIT_FAILURE
#include <boost/program_options.hpp>


	namespace po = boost::program_options;
/*
 * 
 * https://gist.github.com/ksimek/4a2814ba7d74f778bbee
 * 
 */

    // Boost doesn't offer any obvious way to construct a usage string
    // from an infinite list of positional parameters.  This hack
    // should work in most reasonable cases.
    std::vector<std::string> get_unlimited_positional_args_(const po::positional_options_description& p)
    {
        assert(p.max_total_count() == std::numeric_limits<unsigned>::max());

        std::vector<std::string> parts;

        // reasonable upper limit for number of positional options:
        const int MAX = 1000; 
        std::string last = p.name_for_position(MAX);

        for(size_t i = 0; true; ++i)
        {
            std::string cur = p.name_for_position(i);
            if(cur == last)
            {
                parts.push_back(cur);
                parts.push_back('[' + cur + ']');
                parts.push_back("...");
                return parts;
            }
            parts.push_back(cur);
        }
        return parts; // never get here
    }

    std::string make_usage_string_(const std::string& program_name, const po::options_description& desc, po::positional_options_description& p)
    {
        std::vector<std::string> parts;
        parts.push_back("Usage: ");
        parts.push_back(program_name);
        size_t N = p.max_total_count();
        if(N == std::numeric_limits<unsigned>::max())
        {
            std::vector<std::string> args = get_unlimited_positional_args_(p);
            parts.insert(parts.end(), args.begin(), args.end());
        }
        else
        {
            for(size_t i = 0; i < N; ++i)
            {
                parts.push_back(p.name_for_position(i));
            }
        }
        if(desc.options().size() > 0)
        {
            parts.push_back("[options]");
        }
        std::ostringstream oss;
        std::copy(
                parts.begin(),
                parts.end(),
                std::ostream_iterator<std::string>(oss, " "));
        oss << '\n' << desc;
        return oss.str();
    }


    std::string basename_(const std::string& p)
    {
#ifdef HAVE_BOOST_FILESYSTEM
        return boost::filesystem::path(p).stem().string();
#else
        size_t start = p.find_last_of("/");
        if(start == std::string::npos)
            start = 0;
        else
            ++start;
        return p.substr(start);
#endif
    }


/*
 * 
 */



int parse_program_options(int argc, char **argv) {


    
    // for holding onto positional argument values 
    int floor;
    int ceiling;

    
    // named argument descriptions
    po::options_description desc{"Allowed options"};    
    desc.add_options()
        ("help,h", "display help message")
    ;

    
    // positional argument descriptions - hidden from the help screen
    po::options_description hidden_desc;
    hidden_desc.add_options()
        ("floor", po::value<int>(&floor)/*->required()*/, "floor of password size to generate")
        ("ceiling", po::value<int>(&ceiling)/*->required()*/, "non-inclusive ceiling of password size to generate")
    ;


    // add all the descriptions 
    po::options_description all_desc;
    all_desc.add(desc);
    all_desc.add(hidden_desc);
    
    po::positional_options_description positional_desc;
    positional_desc.add("floor", 1);
    positional_desc.add("ceiling", 1);
    
    
    // parse caller input
    po::variables_map vm;
    
    po::parsed_options parsed = 
        po::command_line_parser(argc, argv).options(all_desc)
                                           .positional(positional_desc)
                                           .run();
    po::store(parsed, vm);
    po::notify(vm);
    
    
    // respond to caller input
    if (vm.count("help")) {
        std::cout << make_usage_string_(basename_(argv[0]), desc, positional_desc) << '\n';
    }
    
    
    
	return EXIT_SUCCESS;
}






int main(int argc, char **argv) {
    int parse_program_options_rc = parse_program_options(argc, argv);
    return parse_program_options_rc;
}



