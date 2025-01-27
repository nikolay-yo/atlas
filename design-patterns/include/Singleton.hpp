namespace DesignPattern
{
    class Singleton
    {
    public:
        Singleton( Singleton const& ) = delete;
        Singleton& operator=( Singleton const& ) = delete;

        static std::shared_ptr<Singleton> GetInstance();
        static void Restart();

        void ShowMessage() const;

    private:
        Singleton() {}
        static std::shared_ptr<Singleton> m_instance;
        static std::once_flag m_flag;
    };
}


