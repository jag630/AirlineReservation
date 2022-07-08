# Jacob Goodman
# CSCI T599 Intro to Comp and Prog
# Assignment 5 Airline Program
# July 7 2022 10:00pm

import tkinter as tk
import tkinter.ttk as ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.name_selected = ''
        self.name_list = []
        self.nlist_first_last = []
        self.seats = []
        self.name_list = open("names.txt").read().split("\n")
        self.alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for i in range(20):
            self.seats.append([])
            for j in range(7):
                if j in [1, 3, 5]:
                    self.seats[i].append("COVID")
                else:
                    self.seats[i].append("OPEN")

        for i in self.name_list:
            self.nlist_first_last.append(i.split())

        nlist_first_last = sorted(self.nlist_first_last, key=lambda x: x[1])
        # Source for sorting 2d list by second element:
        # https://stackoverflow.com/questions/20099669/sort-multidimensional-array-based-on-2nd-element-of-the-subarray

        self.name_list.clear()
        for i in nlist_first_last:
            self.name_list.append(" ".join(i))

        # Tkinter widgets below
        self.title("Goody Airlines Reservation Manager")
        self.columnconfigure(0, weight=1, minsize=150)
        self.list_frame = tk.Frame(master=self, pady=10)
        self.list_frame.grid(row=0, column=0, rowspan=13, sticky=tk.N + tk.S)
        self.names = tk.StringVar(value=self.name_list)
        self.listbox = tk.Listbox(
            master=self.list_frame,
            listvariable=self.names,
            height=20
        )
        self.listbox.pack()
        self.listbox.bind('<<ListboxSelect>>', self.select_name)
        self.button_frame = tk.Frame(master=self.list_frame, pady=5)
        self.button_frame.pack()
        self.seat_button = tk.Button(master=self.button_frame, text="Seat/Print Pass", command=self.seat)
        self.seat_button.pack()

        for i in range(1, 8):
            self.columnconfigure(i, weight=1, minsize=50)
        for i in range(13):
            self.rowconfigure(i, weight=1, minsize=20)

        for i in range(1, 8):
            if i == 4:
                aisle_pad = (2, 50)
            else:
                aisle_pad = 2
            for j in range(13):
                frame = tk.Frame(master=self)
                frame.grid(row=j, column=i, padx=aisle_pad, pady=2)
                button = tk.Button(master=frame, text=self.alpha[j] + str(i),
                                   command=lambda row=j, col=i: BoardingPass(self, row, col))
                button.pack(padx=2, pady=2)

    def boarding_pass(self, row, column):
        window = BoardingPass(self, row, column)

    def seat(self):
        for i in range(20):
            for j in range(7):
                if self.seats[i][j] == "OPEN":
                    self.seats[i][j] = self.name_selected
                    print(self.seats)
                    self.name_list.remove(self.name_selected)
                    self.listbox.delete(self.listbox.curselection())
                    BoardingPass(self, i, j+1)

                    return

    def select_name(self, event):
        self.name_selected = self.name_list[self.listbox.curselection()[0]]


class BoardingPass(tk.Toplevel):
    def __init__(self, parent, row, column):
        super().__init__(parent)
        self.title("Boarding Pass")
        tk.Label(self, text="Seat: " + parent.alpha[row] + str(column)).pack()
        ttk.Label(self, text="Name: " + parent.seats[row][column - 1]).pack()
        self.grab_set()


if __name__ == "__main__":
    app = App()
    app.mainloop()
