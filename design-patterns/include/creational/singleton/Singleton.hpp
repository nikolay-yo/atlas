#include <memory>
#include <mutex>

namespace DesignPattern
{
    class Singleton
    {
    private:
        Singleton();// {};
    public:
        Singleton( Singleton const& ) = delete;
        Singleton& operator=( Singleton const& ) = delete;

        static std::shared_ptr<Singleton>& GetInstance();
        static void Restart();

        void ShowMessage() const;

    private:
        static std::shared_ptr<Singleton> c_instance;
        static std::once_flag m_flag;
    };
}


