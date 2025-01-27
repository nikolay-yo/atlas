#include <include/Singleton.hpp>

using namespace DesignPattern;

std::shared_ptr<Singleton> Singleton::GetInstance()
{
    if ( m_instance = null_ptr )
    {
        std::call_once(m_flag, []() {
            m_instance = std::make_shared<Singleton>();
        });
    }

    return m_instance;
}

void Singleton::Restart()
{
    if ( m_instance != null_ptr )
    {
        std::call_once(m_flag, []() {
            m_instance = null_ptr;
        });
    }
}

void Singleton::ShowMessage() const
{
    std::cout << "Hello from Singleton." << std::endl;
}

Singleton::Singleton() {}
std::shared_ptr<Singleton> Singleton::m_instance = null_ptr;
std::once_flag Singleton::flag;

