#include <creational/singleton/Singleton.hpp>

using namespace DesignPattern;

int main() {
    // Accessing the Singleton in multiple threads
    std::shared_ptr<Singleton> singleton = Singleton::GetInstance();
    singleton->ShowMessage();

    // Further access to the Singleton will not create a new instance
    std::shared_ptr<Singleton> singleton2 = Singleton::GetInstance();
    singleton2->ShowMessage();

    return 0;
}

