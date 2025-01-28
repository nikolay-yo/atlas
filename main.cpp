#include <include/Singleton.hpp>

using DesignPattern;

int main() {
    // Accessing the Singleton in multiple threads
    std::shared_ptr<Singleton> singleton = Singleton::GetInstance();
    singleton->showMessage();

    // Further access to the Singleton will not create a new instance
    Singleton* singleton2 = Singleton::GetInstance();
    singleton2->showMessage();

    return 0;
}