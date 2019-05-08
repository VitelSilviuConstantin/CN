from tkinter import *
import tema2

root = Tk()
root.title("Tema2 CN GUI")
root.geometry("400x400")


compute_frame = Frame(root)
compute_frame.grid(row = 0, column = 0)

title_label = Label(compute_frame, text = "Input matrix data")
title_label.grid(row = 0, columnspan = 3)

matrix_entry = []
b_entry = []

def solve_and_print(matrix_entry, b_entry):
    input_matrix = []

    for i in range(3):
        matrix_row = []
        for j in range(3):
            matrix_row.append(float(matrix_entry[i][j].get()))
        input_matrix.append(matrix_row)

    b_matrix = []
    for i in range(3):
        b_matrix.append(float(b_entry[i].get()))

    solution = tema2.solve(input_matrix, b_matrix, 3)

    sol_label = Label(compute_frame, text=str(solution))
    sol_label.grid(row=8, column=0, columnspan=3)


for i in range(1, 4):
    entry_list = []
    for j in range(3):
        entry = Entry(compute_frame)
        entry.grid(row=i, column=j)
        entry_list.append(entry)
    matrix_entry.append(entry_list)

for i in range(3):
    entry = Entry(compute_frame)
    entry.grid(row = 6, column = i)
    b_entry.append(entry)

solve_btn = Button(compute_frame, text = "Solve sistem",
                           command = lambda:solve_and_print(matrix_entry, b_entry), width = 20)
solve_btn.grid(row = 7, columnspan = 3)
root.mainloop()

