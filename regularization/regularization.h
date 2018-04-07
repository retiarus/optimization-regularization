#ifndef _REGULARIZATION_
#ifdef  _REGULARIZATION_

#include <math>

class TikonovOrder0
{
  // public methods 
  public:
    // default constructor
    TikonovOrder0(const int& Nx);

    // operator overloading call
    double operator() (const double& f[], const int& Nx);

  // public atributes
  public:
    string name = '';

  // private atributes
  private:
    float _Nx;
}

#endif
