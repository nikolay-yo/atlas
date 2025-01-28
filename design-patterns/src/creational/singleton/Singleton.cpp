#include <creational/singleton/Singleton.hpp>
#include <iostream>

using namespace DesignPattern;

std::shared_ptr<Singleton>& Singleton::GetInstance()
{
    if ( c_instance = nullptr )
    {
        std::call_once(m_flag, []() {
           c_instance = std::shared_ptr<Singleton>(new Singleton());
        });
    }

    return c_instance;
}

void Singleton::Restart()
{
    if ( c_instance != nullptr )
    {
        std::call_once(m_flag, []() {
            c_instance = nullptr;
        });
    }
}

Singleton::Singleton()
{
}

void Singleton::ShowMessage() const
{
    std::cout << "Hello from Singleton." << std::endl;
}


std::shared_ptr<Singleton> Singleton::c_instance = nullptr;
std::once_flag Singleton::m_flag;

