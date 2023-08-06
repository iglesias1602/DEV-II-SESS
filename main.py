import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk

BASE_NUMBER = 40


class Products:
    def __init__(self):
        self.products = [
            {
                "number": BASE_NUMBER + 0,
                "name": "Cola",
                "price": 1.50,
                "image": "cola.png",
            },
            {
                "number": BASE_NUMBER + 1,
                "name": "Chips",
                "price": 1.00,
                "image": "chips.png",
            },
            {
                "number": BASE_NUMBER + 2,
                "name": "Candy",
                "price": 0.75,
                "image": "candy.png",
            },
            {
                "number": BASE_NUMBER + 3,
                "name": "Water",
                "price": 0.90,
                "image": "water.png",
            },
            {
                "number": BASE_NUMBER + 4,
                "name": "Chips2",
                "price": 1.25,
                "image": "chips_paprika.png",
            },
            {
                "number": BASE_NUMBER + 5,
                "name": "snickers",
                "price": 2.00,
                "image": "snickers.png",
            },
            # Add more products as needed
        ]

    def get_products(self):
        return self.products


class Inventory:
    def __init__(self):
        self.products_data = Products()
        self.stock = {
            product["number"]: 5 for product in self.products_data.get_products()
        }

    def decrease_stock(self, product_number):
        if product_number in self.stock:
            self.stock[product_number] -= 1

    def get_stock(self, product_number):
        return self.stock.get(product_number, 0)


class Transaction:
    def __init__(self, app):
        self.app = app
        self.selected_number = ""
        self.countdown_id = None

    def on_num_button_click(self, button):
        if button == "#":
            self.process_selected_number()
        else:
            self.selected_number += button
            self.app.typed_number_label.config(text=self.selected_number)
            if self.countdown_id:
                # If there is a scheduled countdown, cancel it before starting a new one
                self.app.after_cancel(self.countdown_id)
            self.countdown_id = self.app.after(2000, self.process_selected_number)

    def clear_typed_number(self):
        self.selected_number = ""
        self.app.typed_number_label.config(text="")
        if self.countdown_id:
            # If the "Clear" button is clicked, cancel any scheduled countdown
            self.app.after_cancel(self.countdown_id)
            self.countdown_id = None

    def process_selected_number(self):
        self.countdown_id = None

        if self.selected_number:
            product_number = int(self.selected_number)
            selected_product = self.get_selected_product(product_number)

            if selected_product:
                stock_left = self.app.inventory.get_stock(product_number)

                if (
                    self.app.current_coins >= selected_product["price"]
                    and stock_left > 0
                ):
                    self.app.current_coins -= selected_product["price"]
                    self.app.update_coin_label()
                    self.process_successful_purchase(selected_product, stock_left)
                elif stock_left == 0:
                    self.show_out_of_stock_message(selected_product)
                else:
                    self.show_insufficient_coins_message(selected_product)
            else:
                self.show_invalid_product_message()

        self.clear_typed_number()

    def get_selected_product(self, product_number):
        return next(
            (
                product
                for product in self.app.products_data.get_products()
                if product["number"] == product_number
            ),
            None,
        )

    def process_successful_purchase(self, selected_product, stock_left):
        self.app.inventory.decrease_stock(selected_product["number"])
        stock_left = self.app.inventory.get_stock(selected_product["number"])
        messagebox.showinfo(
            "Purchase Successful", f"You purchased {selected_product['name']}."
        )
        self.show_stock_left_message(stock_left, selected_product)

    def show_out_of_stock_message(self, selected_product):
        messagebox.showerror(
            "Out of Stock", f"{selected_product['name']} is out of stock."
        )

    def show_insufficient_coins_message(self, selected_product):
        messagebox.showinfo(
            "Insufficient Coins", "You do not have enough coins for this product."
        )

    def show_invalid_product_message(self):
        messagebox.showinfo(
            "Invalid Product Number", "Please enter a valid product number."
        )

    def show_stock_left_message(self, stock_left, selected_product):
        messagebox.showinfo(
            "Stock Left", f"{stock_left} {selected_product['name']}(s) left."
        )


class CoinInputWindow(tk.Toplevel):
    def __init__(self, parent, add_coin_callback):
        super().__init__(parent)
        self.title("Coin Input")
        self.geometry("250x200")

        coin_values = ["0.05", "0.10", "0.20", "1.00", "2.00"]
        for i, coin_value in enumerate(coin_values):
            coin_button = tk.Button(
                self,
                text=f"Add ${coin_value}",
                command=lambda value=coin_value: add_coin_callback(float(value)),
            )
            coin_button.grid(row=i // 2, column=i % 2, padx=5, pady=5)

        clear_button = tk.Button(self, text="Clear", command=self.clear_and_close)
        clear_button.grid(
            row=len(coin_values) // 2, column=3, columnspan=2, padx=5, pady=5
        )

    def clear_and_close(self):
        self.master.clear_coins()
        self.destroy()


class VendingMachineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vending Machine Simulator")
        self.geometry("650x840")  # Set a larger size for the main window

        # Call the method to set the background image
        self.set_background()

        # Create a list to store all the PhotoImage instances for the product images
        self.product_images = []

        # Create a Products and inventory instance to access the product data
        self.products_data = Products()
        self.inventory = Inventory()

        # Initialize variables for coin input and user selection
        self.current_coins = 0.0
        self.selected_product = None
        self.selected_number = ""

        # Create a dictionary to store the quantity of each product
        self.product_quantities = {
            product["number"]: tk.IntVar()
            for product in self.products_data.get_products()
        }

        # Create the vending machine grid
        self.create_vending_grid()

        # Create the 'buy' button
        self.create_buy_button()

        # Create the numpad
        self.transaction = Transaction(self)
        self.create_numpad()

        # Variable to store the id of the scheduled countdown
        self.countdown_id = None

    def set_background(self):
        # Load the image file
        bg_image = tk.PhotoImage(file="assets/img/background.png")

        # Create a label to display the background image and make it fill the entire window
        bg_label = tk.Label(self, image=bg_image)
        bg_label.place(x=-175, y=0, anchor="nw")

        # Make sure to keep a reference to the image, otherwise it will be garbage collected
        bg_label.image = bg_image

    def create_vending_grid(self):
        max_product_number = (
            BASE_NUMBER + 29
        )  # The maximum product number you want to display

        # Create a dictionary to store the product number and its corresponding image
        product_images_dict = {}

        for product in self.products_data.get_products():
            number = product["number"]
            image_path = f"assets/img/{product['image']}"

            if number <= max_product_number:
                name = product["name"]
                price = product["price"]
                image_path = f"assets/img/{product['image']}"

                # Open the image using Pillow
                img_pil = Image.open(image_path)

                # Calculate the downsampling factor to limit the dimensions to 50x50 pixels
                img_pil.thumbnail((50, 50))

                # Convert the Pillow image to ImageTk format for tkinter
                img = ImageTk.PhotoImage(img_pil)

                # Store the image in the dictionary
                product_images_dict[number] = img

                # Append the PhotoImage instance to the product_images list
                self.product_images.append(img)

                # Create and display the image label
                row = (number - BASE_NUMBER) // 5
                col = (number - BASE_NUMBER) % 5

                image_label = tk.Label(self, image=img)
                image_label.image = img
                image_label.grid(row=row + 1, column=col, padx=5, pady=5)
                image_label.place(x=col * 45 + 122, y=row * 73 + 153, anchor="center")

                # Create and display the product number label
                info_label_number = tk.Label(self, text=f"{number}")
                info_label_number.grid(row=row + 1, column=col, padx=5, pady=5)
                info_label_number.place(
                    x=col * 45 + 122, y=row * 73 + 175, anchor="center"
                )

                # Create and display the product price label
                info_label = tk.Label(self, text=f"€{price:.2f}")
                info_label.grid(row=row + 1, column=col, padx=5, pady=5)
                info_label.place(x=col * 45 + 122, y=row * 73 + 190, anchor="center")

        # Create empty slot labels for product numbers without products
        for number in range(BASE_NUMBER, max_product_number + 1):
            if number not in product_images_dict:
                row = (number - BASE_NUMBER) // 5
                col = (number - BASE_NUMBER) % 5

                empty_slot_label = tk.Label(
                    self,
                    text="🚫",
                    font=("Arial", 18),
                    fg="red",
                )
                empty_slot_label.pack()

                empty_slot_label.grid(row=row + 1, column=col, padx=5, pady=5)
                empty_slot_label.place(
                    x=col * 45 + 123, y=row * 73 + 150, anchor="center"
                )

    def create_buy_button(self):
        buy_button = tk.Button(
            self,
            text="Buy",
            command=self.show_coin_input_window,
            bg="green",
            fg="white",
            font=("Arial", 10),
        )
        buy_button.grid(row=1, column=2, padx=5, pady=5)
        buy_button.place(x=375, y=245, anchor="center")

    def show_coin_input_window(self):
        coin_input_window = CoinInputWindow(self, self.add_coin)

    def add_coin(self, value):
        self.current_coins += value
        self.update_coin_label()

    def clear_coins(self):
        self.current_coins = 0.0
        self.update_coin_label()

    def update_coin_label(self):
        self.coin_amount_label.config(text=f"Current Coins: ${self.current_coins:.2f}")

    def create_numpad(self):
        # List of product numbers for the numpad
        num_pad = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "0", "#"]

        # Create buttons for each number in the numpad
        for i, number in enumerate(num_pad):
            row = i // 3
            col = i % 3 + 5  # Adjusted column to align correctly

            if number in {"*", "#"}:
                num_button = tk.Button(
                    self,
                    text=number,
                    width=3,  # Adjust the width of the button to make it larger
                    height=2,
                    command=lambda: None,  # Disable the button click events
                    state=tk.DISABLED,  # Set the state to disabled
                    font=("Arial", 12),
                    bg="lightgray",
                )
            else:
                num_button = tk.Button(
                    self,
                    text=number,
                    width=3,  # Adjust the width of the button to make it larger
                    height=2,  # Adjust the height of the button to make it larger
                    command=lambda num=number: self.on_num_button_click(num),
                    font=("Arial", 12),
                    bg="lightgray",
                )

            num_button.grid(
                row=row + 5, column=col, columnspan=10, padx=2, pady=2
            )  # Adjusted row to start from 5

            # Move the numpad 500 pixels to the left
            num_button.place(x=275 + col * 40, y=260 + row * 52)

        # Create a label to display the typed number
        self.typed_number_label = tk.Label(
            self,
            text="",
            font=("Arial", 16),
            bg="lightgray",
            padx=10,
            pady=5,
            width=8,
        )
        self.typed_number_label.grid(
            row=4, column=6, columnspan=3, padx=5, pady=5
        )  # Adjusted column and columnspan

        # Create a label to display the current coin amount
        self.coin_amount_label = tk.Label(self, text="Current Coins: $0.00")
        self.coin_amount_label.grid(
            row=5, column=0, columnspan=len(num_pad) + 4, padx=5, pady=5
        )  # Adjusted the columnspan
        self.coin_amount_label.place(x=535, y=200, anchor="center")

        self.typed_number_label.place(x=195 + col * 40, y=60 + row * 52)

    def clear_typed_number(self):
        self.transaction.clear_typed_number()

    def process_selected_number(self):
        self.transaction.process_selected_number()

    def on_num_button_click(self, number):
        self.transaction.on_num_button_click(number)


if __name__ == "__main__":
    app = VendingMachineApp()
    app.mainloop()
