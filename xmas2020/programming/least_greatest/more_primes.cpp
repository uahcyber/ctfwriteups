#include <iostream>
#include <gmpxx.h>

template<typename Integer, typename OutputIterator>
 void decompose(Integer n, OutputIterator out)
{
    Integer i(2);
 
    while (n != 1)
    {
        while (n % i == Integer(0))
        {
            *out++ = i;
            n /= i;
        }
        ++i;
    }
}

template<typename T> class infix_ostream_iterator:
    public std::iterator<T, std::output_iterator_tag>
{
    class Proxy;
    friend class Proxy;
    class Proxy
    {
    public:
        Proxy(infix_ostream_iterator& iter): iterator(iter) {}
        Proxy& operator=(T const& value)
        {
            if (!iterator.first)
            {
                iterator.stream << iterator.infix;
            }
            iterator.stream << value;
        }
    private:
        infix_ostream_iterator& iterator;
    };
public:
    infix_ostream_iterator(std::ostream& os, char const* inf):
        stream(os),
        first(true),
        infix(inf)
    {
    }
    infix_ostream_iterator& operator++() { first = false; return *this; }
    infix_ostream_iterator operator++(int)
    {
        infix_ostream_iterator prev(*this);
        ++*this;
        return prev;
    }
    Proxy operator*() { return Proxy(*this); }
private:
    std::ostream& stream;
    bool first;
    char const* infix;
};
 
int main(int argc, char* argv[])
{
    if (argc < 2) {
        std::cout << "Incorrect usage\n";
        return -1;
    }
    mpz_class number;
    number = argv[1];
 
    if (number <= 0)
        std::cout << "this number is not positive!\n";
    else {
        decompose(number, infix_ostream_iterator<mpz_class>(std::cout, ","));
        std::cout << "\n";
    }
}