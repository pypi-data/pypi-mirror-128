from nehushtan.matrix.LinearAlgebra.Matrix import Matrix


def test1():
    data = [
        [1, 2, 3],
        [0, -6, 7]
    ]
    m1 = Matrix(data)
    print('M1')
    print(m1)

    m2 = m1.do_operation_addition(m1)
    print('M2=M1+M1')
    print(m2)

    m3 = m1.do_operation_scalar_multiplication(-1)
    print('M3=M1*(-1)')
    print(m3)

    m4 = m1.do_operation_transposition()
    print('M4=M1^T')
    print(m4)

    m5 = m1.do_operation_matrix_multiplication(m4)
    print('M5=M1 * M4')
    print(m5)


if __name__ == '__main__':
    test1()
