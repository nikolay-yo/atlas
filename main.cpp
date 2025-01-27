#include <include/Singleton.hpp>

using DesignPattern;

int main() {
    // Accessing the Singleton in multiple threads
    Singleton* singleton = Singleton::getInstance();
    singleton->showMessage();

    // Further access to the Singleton will not create a new instance
    Singleton* singleton2 = Singleton::getInstance();
    singleton2->showMessage();

    return 0;
}