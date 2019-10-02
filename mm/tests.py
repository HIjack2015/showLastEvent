# Function defined outside the class
def f1(self, x, y):
    return min(x, x+y)
class C:
    f = f1

    def g(self):
        return 'hello world'

    h = g
    int

class D:
    f = f1

    def g(self):
        return 'hello world'

    h = g


f1(C,1,2)
c=C()
c.f1(1,3)

d=D()
d.f1(1,3)