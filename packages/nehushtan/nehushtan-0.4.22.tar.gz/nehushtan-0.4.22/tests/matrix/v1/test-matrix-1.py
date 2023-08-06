from nehushtan.matrix.v1.Matrix import Matrix


def test1():
    data_1 = {
        "Name": [
            "Braund, Mr. Owen Harris",
            "Allen, Mr. William Henry",
            "Bonnell, Miss. Elizabeth",
        ],
        "Age": [22, 35, 58],
        "Sex": ["male", "male", "female"],
    }
    matrix_1 = Matrix(data_1)
    print(matrix_1)

    print(" ===== CAHNGE Age OF Allen TO 100 ===== ")
    matrix_1.update_cell(1, "Age", 100)
    print(matrix_1)

    print(" ===== ADD ROW Brande ===== ")
    matrix_1.append_one_row({
        "Name": "Brande, Mr. Hari Kane",
        "Age": 39,
        "Sex": "male"
    })
    print(matrix_1)

    print(" ===== ADD COLUMN Address ===== ")
    matrix_1.append_one_column(
        'Address',
        [
            "New York",
            "New Jersey",
            "New Sedney",
            "New Mexico",
        ]
    )
    print(matrix_1)


if __name__ == '__main__':
    test1()
