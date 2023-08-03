import tkinter as tk
from tkinter import simpledialog, messagebox

class Products:
    def __init__(self):
        self.products = [
            {"number": 1, "name": "Cola", "price": 1.50, "image": "cola.png"},
            {"number": 2, "name": "Chips", "price": 1.00, "image": "chips.png"},
            {"number": 3, "name": "Candy", "price": 0.75, "image": "candy.png"},
            {"number": 4, "name": "Water", "price": 0.90, "image": "water.png"},
            # Add more products as needed
        ]

    def get_products(self):
        return self.products

class VendingMachineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vending Machine Simulator")
        self.geometry("800x500")  # Set a larger size for the main window


        # Create a Products instance to access the product data
        self.products_data = Products()

        # Initialize variables for coin input and user selection
        self.current_coins = 0.0
        self.selected_product = None
        self.selected_number = ""

        # Create a dictionary to store the quantity of each product
        self.product_quantities = {product["number"]: tk.IntVar() for product in self.products_data.get_products()}

        # Create the vending machine grid
        self.create_vending_grid()

        # Create the coin input section
        self.create_coin_input()

        # Create the numpad
        self.create_numpad()

        # Variable to store the id of the scheduled countdown
        self.countdown_id = None

    def create_vending_grid(self):
        for product in self.products_data.get_products():
            number = product["number"]
            name = product["name"]
            price = product["price"]
            image_path = product["image"]

            # Load the image from the file
            img = tk.PhotoImage(file=image_path)

            # Calculate the downsampling factor to limit the dimensions to 70x70 pixels
            width = img.width()
            height = img.height()
            downsample_factor = max(1, width // 70, height // 70)

            # Resize the image by downsampling
            img = img.subsample(downsample_factor)

            # Create a label to display the image
            image_label = tk.Label(self, image=img)
            image_label.image = img
            image_label.grid(row=number, column=1, padx=5, pady=5)

            # Create a label to display the product number, name, and price
            info_label = tk.Label(self, text=f"{number}. {name} - ${price:.2f}")
            info_label.grid(row=number, column=0, padx=5, pady=5)

    def create_coin_input(self):
        # List of coin values to add
        coin_values = ["0.05", "0.10", "0.20", "1.00", "2.00"]

        # Create buttons for each coin value to add
        for i, coin_value in enumerate(coin_values):
            coin_button = tk.Button(self, text=f"Add ${coin_value}", command=lambda value=coin_value: self.add_coin(float(value)))
            coin_button.grid(row=2, column=i+2, padx=5, pady=5)  # Adjusted the row and column indices

        # Create the "Clear" button to reset the current coin value
        clear_button = tk.Button(self, text="Clear", command=self.clear_coins)
        clear_button.grid(row=2, column=len(coin_values)+2, padx=5, pady=5)  # Adjusted the column index

        # Create a label to display the current coin amount
        self.coin_amount_label = tk.Label(self, text="Current Coins: $0.00")
        self.coin_amount_label.grid(row=3, column=0, columnspan=len(coin_values) + 7, padx=5, pady=5)  # Adjusted the columnspan




    def create_numpad(self):
        # List of product numbers for the numpad
        num_pad = [
            "1", "2", "3",
            "4", "5", "6",
            "7", "8", "9",
            "*", "0", "#"
        ]

        # Create buttons for each number in the numpad
        for i, number in enumerate(num_pad):
            row = i // 3
            col = i % 3 + 6  # Adjusted column to align correctly

            num_button = tk.Button(self, text=number, command=lambda num=number: self.on_num_button_click(num))
            num_button.grid(row=row + 5, column=col+2, padx=2, pady=2)  # Adjusted row to start from 5

        # Create a label to display the typed number
        self.typed_number_label = tk.Label(self, text="", font=("Arial", 16), bg="lightgray", padx=10, pady=5)
        self.typed_number_label.grid(row=4, column=8, columnspan=3, padx=5, pady=5)  # Adjusted column and columnspan

    def add_coin(self, value):
        self.current_coins += value
        self.update_coin_label()

    def clear_coins(self):
        self.current_coins = 0.0
        self.update_coin_label()

    def update_coin_label(self):
        self.coin_amount_label.config(text=f"Current Coins: ${self.current_coins:.2f}")

    def on_num_button_click(self, button):
        if button == "#":
            self.process_selected_number()
        else:
            self.selected_number += button
            self.typed_number_label.config(text=self.selected_number)
            if self.countdown_id:
                # If there is a scheduled countdown, cancel it before starting a new one
                self.after_cancel(self.countdown_id)
            self.countdown_id = self.after(2000, self.process_selected_number)

    def clear_typed_number(self):
        self.selected_number = ""
        self.typed_number_label.config(text="")
        if self.countdown_id:
            # If the "Clear" button is clicked, cancel any scheduled countdown
            self.after_cancel(self.countdown_id)
            self.countdown_id = None

    def process_selected_number(self):
        self.countdown_id = None
        if self.selected_number:
            product_number = int(self.selected_number)
            selected_product = next((product for product in self.products if product["number"] == product_number), None)

            if selected_product:
                if self.current_coins >= selected_product["price"]:
                    self.current_coins -= selected_product["price"]
                    self.update_coin_label()
                    messagebox.showinfo("Purchase Successful", f"You purchased {selected_product['name']}.")
                else:
                    messagebox.showinfo("Insufficient Coins", "You do not have enough coins for this product.")
            else:
                messagebox.showinfo("Invalid Product Number", "Please enter a valid product number.")

        self.clear_typed_number()  # Auto-clear the typed number after purchase or error

if __name__ == "__main__":
    app = VendingMachineApp()
    app.mainloop()
