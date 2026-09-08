#include <iostream>

#include "gpucfr.h"


int main (int argc, char ** argv) {
    if (argc != 3) {
        std::cerr << "Run the program with two parameters - <int: number of iterations> <string: efg game file path>" << std::endl;
        return 1;
    }
    unsigned int iterations = strtol(argv[1], nullptr, 0);
    std::string gamepath(argv[2]);

    GPUCFR instance = GPUCFR(gamepath);
    instance.run_iterations(iterations);
    instance.print_average_strategy();

    return 0;

}
