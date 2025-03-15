#include <string>
#include "bar.h"
#include "foo.h"

std::string bar() {
  return foo() + std::string("bar");
}
