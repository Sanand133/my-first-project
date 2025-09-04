import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox
import random
from tkcalendar import Calendar  
from datetime import datetime

class Room:
    """
    Represents a hotel room.
    """
    def __init__(self, room_number, is_ac=False, is_double_bed=False, is_booked=False, customer_name="", check_in="", check_out=""):
        """Initializes a Room object."""
        self.room_number = room_number
        self.is_ac = is_ac
        self.is_double_bed = is_double_bed
        self.is_booked = is_booked
        self.customer_name = customer_name
        self.check_in = check_in
        self.check_out = check_out

    def __repr__(self):
        """
        Returns a string representation of the Room object.
        """
        return f"Room(number={self.room_number}, AC={self.is_ac}, DoubleBed={self.is_double_bed}, Booked={self.is_booked}, Customer={self.customer_name}, CheckIn={self.check_in}, CheckOut={self.check_out})"

    def __eq__(self, other):
        """
        Overrides the default implementation.
        """
        if not isinstance(other, Room):
            return NotImplemented
        return (self.room_number == other.room_number and
                self.is_ac == other.is_ac and
                self.is_double_bed == other.is_double_bed and
                self.is_booked == other.is_booked and
                self.customer_name == other.customer_name and
                self.check_in == other.check_in and
                self.check_out == other.check_out)


class HotelManager:
    """
    Manages hotel rooms and their data.
    """
    def __init__(self):
        """Initializes the HotelManager."""
        self.rooms = []
        self.script_dir = os.path.dirname(os.path.abspath(__file__))  
        self.csv_file = os.path.join(self.script_dir, "hotel_rooms.csv")  
        self.initialize_rooms()

    def initialize_rooms(self):
        """Initialize rooms with random AC/double bed options"""
        if os.path.exists(self.csv_file):
            self.load_from_csv()
        else:
            self.rooms = []
            for i in range(1, 46):  
                self.rooms.append(Room(
                    room_number=i,
                    is_ac=random.choice([True, False]),
                    is_double_bed=random.choice([True, False])
                ))
            self.save_to_csv()

    def save_to_csv(self):
        """Save all room data to CSV file"""
        with open(self.csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "RoomNumber", "AC", "DoubleBed", "Booked",
                "CustomerName", "CheckInDate", "CheckOutDate"
            ])
            for room in self.rooms:
                writer.writerow([
                    room.room_number,
                    int(room.is_ac),
                    int(room.is_double_bed),
                    int(room.is_booked),
                    room.customer_name,
                    room.check_in,
                    room.check_out
                ])

    def load_from_csv(self):
        """Load room data from CSV file"""
        self.rooms = []
        with open(self.csv_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  
            for row in reader:
                self.rooms.append(Room(
                    room_number=int(row[0]),
                    is_ac=bool(int(row[1])),
                    is_double_bed=bool(int(row[2])),
                    is_booked=bool(int(row[3])),
                    customer_name=row[4],
                    check_in=row[5],
                    check_out=row[6]
                ))

    def get_all_rooms(self):
        """Return all rooms"""
        return self.rooms

    def get_available_rooms(self, want_ac=None, want_double_bed=None):
        """Filter available rooms by optional criteria"""
        available = []
        for room in self.rooms:
            if not room.is_booked:
                if (want_ac is None or room.is_ac == want_ac) and \
                        (want_double_bed is None or room.is_double_bed == want_double_bed):
                    available.append(room)
        return available

    def book_room(self, room_number, customer_name, check_in, check_out):
        """Book a specific room"""
        if 1 <= room_number <= len(self.rooms):
            room = self.rooms[room_number - 1]
            if not room.is_booked:
                room.is_booked = True
                room.customer_name = customer_name
                room.check_in = check_in
                room.check_out = check_out
                self.save_to_csv()
                return True
        return False

    def check_out(self, room_number):
        """Check out from a room and return booking info"""
        if 1 <= room_number <= len(self.rooms):
            room = self.rooms[room_number - 1]
            if room.is_booked:
                booking_info = {
                    'room_number': room.room_number,
                    'customer': room.customer_name,
                    'period': f"{room.check_in} to {room.check_out}"
                }
                room.is_booked = False
                room.customer_name = ""
                room.check_in = ""
                room.check_out = ""
                self.save_to_csv()
                return (True, booking_info)
        return (False, None)

class HotelGUI:
    """
    Graphical User Interface for the Hotel Management System.
    """
    def __init__(self, root):
        """
        Initializes the HotelGUI.
        """
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("900x600")

        self.hotel = HotelManager()

        self.create_widgets()

    def create_widgets(self):
        """
        Creates and arranges the GUI widgets.
        """
        
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=5)

        ttk.Button(button_frame, text="All Rooms", command=self.show_all_rooms).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Available Rooms", command=self.show_available_rooms).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Book Room", command=self.book_room).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Check Out", command=self.check_out).pack(side=tk.LEFT, padx=5)

        
        self.tree = ttk.Treeview(self.main_frame, columns=('Room', 'AC', 'Bed', 'Status', 'Customer', 'Period'),
                                 show='headings')
        self.tree.pack(fill=tk.BOTH, expand=True)

        
        self.tree.heading('Room', text='Room No.')
        self.tree.heading('AC', text='AC')
        self.tree.heading('Bed', text='Bed Type')
        self.tree.heading('Status', text='Status')
        self.tree.heading('Customer', text='Customer')
        self.tree.heading('Period', text='Booking Period')

        self.tree.column('Room', width=80, anchor=tk.CENTER)
        self.tree.column('AC', width=50, anchor=tk.CENTER)
        self.tree.column('Bed', width=80, anchor=tk.CENTER)
        self.tree.column('Status', width=80, anchor=tk.CENTER)
        self.tree.column('Customer', width=150)
        self.tree.column('Period', width=150)

        
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X, pady=(5, 0))

        
        self.show_all_rooms()

    def show_all_rooms(self):
        """Display all rooms in the treeview"""
        self.clear_tree()
        for room in self.hotel.get_all_rooms():
            status = "Booked" if room.is_booked else "Available"
            customer = room.customer_name if room.is_booked else ""
            period = f"{room.check_in} to {room.check_out}" if room.is_booked else ""

            self.tree.insert('', tk.END, values=(
                room.room_number,
                "Yes" if room.is_ac else "No",
                "Double" if room.is_double_bed else "Single",
                status,
                customer,
                period
            ))
        self.status_var.set(f"Displaying all {len(self.hotel.get_all_rooms())} rooms")

    def show_available_rooms(self):
        """Show available rooms filtering dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Filter Available Rooms")

        ttk.Label(dialog, text="AC Room?").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ac_var = tk.StringVar()
        ttk.Combobox(dialog, textvariable=ac_var, values=["Any", "Yes", "No"], state="readonly").grid(row=0, column=1,
                                                                                                   padx=5, pady=5)
        ac_var.set("Any")

        ttk.Label(dialog, text="Double Bed?").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        bed_var = tk.StringVar()
        ttk.Combobox(dialog, textvariable=bed_var, values=["Any", "Yes", "No"], state="readonly").grid(row=1, column=1,
                                                                                                    padx=5, pady=5)
        bed_var.set("Any")

        def apply_filter():
            want_ac = None if ac_var.get() == "Any" else (ac_var.get() == "Yes")
            want_bed = None if bed_var.get() == "Any" else (bed_var.get() == "Yes")

            available = self.hotel.get_available_rooms(want_ac, want_bed)
            self.clear_tree()

            for room in available:
                self.tree.insert('', tk.END, values=(
                    room.room_number,
                    "Yes" if room.is_ac else "No",
                    "Double" if room.is_double_bed else "Single",
                    "Available",
                    "",
                    ""
                ))

            self.status_var.set(f"Found {len(available)} available rooms matching your criteria")
            dialog.destroy()

        ttk.Button(dialog, text="Apply Filter", command=apply_filter).grid(row=2, column=0, columnspan=2, pady=10)

    def book_room(self):
        """Show room booking dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Book Room")

        ttk.Label(dialog, text="AC Room?").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ac_var = tk.StringVar()
        ttk.Combobox(dialog, textvariable=ac_var, values=["Yes", "No"], state="readonly").grid(row=0, column=1, padx=5,
                                                                                            pady=5)
        ac_var.set("Yes")

        ttk.Label(dialog, text="Double Bed?").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        bed_var = tk.StringVar()
        ttk.Combobox(dialog, textvariable=bed_var, values=["Yes", "No"], state="readonly").grid(row=1, column=1, padx=5,
                                                                                             pady=5)
        bed_var.set("Yes")

        ttk.Button(dialog, text="Find Available Rooms",
                  command=lambda: self.show_available_for_booking(dialog, ac_var.get() == "Yes",
                                                                bed_var.get() == "Yes")) \
            .grid(row=2, column=0, columnspan=2, pady=10)

    def show_available_for_booking(self, parent_dialog, want_ac, want_double_bed):
        """Show available rooms for booking"""
        available = self.hotel.get_available_rooms(want_ac, want_double_bed)
        parent_dialog.destroy()

        if not available:
            messagebox.showinfo("No Rooms", "No matching rooms available.")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Book Available Room")

        ttk.Label(dialog, text="Available Rooms:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        room_var = tk.StringVar()
        ttk.Combobox(dialog, textvariable=room_var,
                         values=[str(r.room_number) for r in available], state="readonly").grid(row=0, column=1, padx=5,
                                                                                            pady=5)
        room_var.set(str(available[0].room_number))

        ttk.Label(dialog, text="Customer Name:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(dialog)
        name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Check-in Date:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        checkin_entry = ttk.Entry(dialog)  
        checkin_entry.grid(row=2, column=1, padx=5, pady=5)
        checkin_cal_button = ttk.Button(dialog, text="Select Date", command=lambda: self.show_calendar(dialog, checkin_entry))
        checkin_cal_button.grid(row=2, column=2, padx=5, pady=5)


        ttk.Label(dialog, text="Check-out Date:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        checkout_entry = ttk.Entry(dialog) 
        checkout_entry.grid(row=3, column=1, padx=5, pady=5)
        checkout_cal_button = ttk.Button(dialog, text="Select Date", command=lambda: self.show_calendar(dialog, checkout_entry))
        checkout_cal_button.grid(row=3, column=2, padx=5, pady=5)


        def confirm_booking():
            try:
                room_num = int(room_var.get())
                customer = name_entry.get()
                check_in = checkin_entry.get()
                check_out = checkout_entry.get()

                if not customer or not check_in or not check_out:
                    messagebox.showerror("Error", "All fields are required!")
                    return

                
                try:
                    datetime.strptime(check_in, "%d/%m/%Y")
                    datetime.strptime(check_out, "%d/%m/%Y")
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format. Please use DD/MM/YYYY")
                    return

                if self.hotel.book_room(room_num, customer, check_in, check_out):
                    messagebox.showinfo("Success", f"Room {room_num} booked successfully!")
                    self.show_all_rooms()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Booking failed. Room may be already booked.")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid information!")

        ttk.Button(dialog, text="Confirm Booking", command=confirm_booking).grid(row=4, column=0, columnspan=3, pady=10)

    def show_calendar(self, parent, entry_widget):
        """
        Displays a calendar widget for date selection.

        Args:
            parent: The parent window.
            entry_widget: The Entry widget to update with the selected date.
        """
        cal_dialog = tk.Toplevel(parent)
        cal_dialog.title("Select Date")
        cal = Calendar(cal_dialog, selectmode='day', date_pattern='dd/mm/yyyy')
        cal.pack(padx=10, pady=10)

        def set_date():
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, cal.get_date())
            cal_dialog.destroy()

        ttk.Button(cal_dialog, text="Set Date", command=set_date).pack(pady=5)


    def check_out(self):
        """Show room checkout dialog"""
        booked_rooms = [r for r in self.hotel.get_all_rooms() if r.is_booked]

        if not booked_rooms:
            messagebox.showinfo("No Bookings", "There are no booked rooms to check out.")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Check Out")

        ttk.Label(dialog, text="Select Room:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        room_var = tk.StringVar()
        ttk.Combobox(dialog, textvariable=room_var,
                         values=[f"{r.room_number} - {r.customer_name}" for r in booked_rooms],
                         state="readonly").grid(row=0, column=1, padx=5, pady=5)
        room_var.set(f"{booked_rooms[0].room_number} - {booked_rooms[0].customer_name}")

        def confirm_checkout():
            room_num = int(room_var.get().split()[0])
            success, booking_info = self.hotel.check_out(room_num)

            if success:
                message = f"Room {booking_info['room_number']} checked out successfully!\n\n"
                message += f"Guest: {booking_info['customer']}\n"
                message += f"Stay: {booking_info['period']}"
                messagebox.showinfo("Check Out Complete", message)
                self.show_all_rooms()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Check-out failed. Room may not be booked.")

        ttk.Button(dialog, text="Confirm Checkout", command=confirm_checkout).grid(row=1, column=0, columnspan=2, pady=10)

    def clear_tree(self):
        """Clear all items from the treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)


if __name__ == "__main__":
    root = tk.Tk()
    app = HotelGUI(root)
    root.mainloop()
