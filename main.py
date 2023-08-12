import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, UnidentifiedImageError

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
                "name": "Snickers",
                "price": 2.00,
                "image": "snickers.png",
            },
            {
                "number": BASE_NUMBER + 13,
                "name": "Granola Bar",
                "price": 1.80,
                "image": "granola_bar.png",
            }
            # Add more products as needed max #69
        ]

    def get_products(self):
        return self.products


class Inventory:
    def __init__(self, products_data):
        self.products_data = products_data
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

        # Call the method to display the copied image after a successful purchase
        self.app.display_copied_image(selected_product["number"])

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
        self.geometry("325x275")

        self.resizable(False, False)

        coin_values = ["0.05", "0.10", "0.20", "1.00", "2.00"]
        coin_images = [
            "coin_5c.png",
            "coin_10c.png",
            "coin_20c.png",
            "coin_1e.png",
            "coin_2e.png",
        ]
        for i, coin_value in enumerate(coin_values):
            img_path = f"assets/img/{coin_images[i]}"
            try:
                coin_img = Image.open(img_path)
                coin_img = coin_img.resize((60, 60))
                coin_img = ImageTk.PhotoImage(coin_img)

                coin_button = tk.Button(
                    self,
                    text=f"Add €{coin_value}",
                    image=coin_img,  # Set the image for the button,
                    compound=tk.LEFT,  # Display the image to the left of the text
                    command=lambda value=coin_value: add_coin_callback(float(value)),
                )
                coin_button.image = coin_img  # Keep a reference to the image to avoid garbage collection

                coin_button.grid(row=i // 2, column=i % 2, padx=5, pady=5)
            except (FileNotFoundError, UnidentifiedImageError):
                print(f"Error: Could not load the image at {img_path}")

        continue_button = tk.Button(
            self,
            text="Continue Transaction",
            command=self.destroy,
            bg="green",
            fg="white",
            font=("Arial", 8, "bold"),
        )
        continue_button.grid(
            row=len(coin_values) // 2 + 1, column=2 - 1, columnspan=5, padx=5, pady=0
        )

        clear_button = tk.Button(
            self,
            text="Cancel Transaction",
            command=self.clear_and_close,
            bg="red",
            fg="white",
            font=("Arial", 8, "bold"),
        )
        clear_button.grid(
            row=len(coin_values) // 2, column=2 - 1, columnspan=2, padx=5, pady=5
        )

    def clear_and_close(self):
        self.master.clear_coins()
        self.destroy()


class ProductManagementWindow(tk.Toplevel):
    def __init__(self, parent, products_data):
        super().__init__(parent)
        self.title("Product Management")
        self.geometry("800x800")

        self.main_app = parent

        self.products_data = products_data
        self.selected_product = None

        self.edit_button = self.create_button("Edit", self.edit_product, x=450, y=100)
        self.delete_button = self.create_button(
            "Delete", self.delete_product, x=450, y=150
        )
        self.add_button = self.create_button("Add", self.add_product, x=450, y=200)
        self.set_buttons_state(disabled=True)

        self.create_product_grid()

        self.previous_selected_button = None

        # Assuming you have an instance of Inventory class named 'inventory'
        inventory = Inventory(products_data)

    def create_button(self, text, command, x, y):
        button = tk.Button(self, text=text, command=command)
        button.place(x=x, y=y)
        return button

    def create_product_grid(self):
        self.cell_buttons = []

        button_width = 60
        button_height = 70

        for row in range(6):
            row_buttons = []
            for col in range(5):
                button = tk.Button(
                    self,
                    text="",
                    width=button_width,
                    height=button_height,
                    command=lambda r=row, c=col: self.on_cell_click(r, c),
                )
                x = col * (button_width + 15) + 20
                y = row * (button_height + 15) + 20
                button.place(x=x, y=y)
                row_buttons.append(button)
            self.cell_buttons.append(row_buttons)

        self.update_cell_buttons()

    def update_cell_buttons(self):
        for row, row_buttons in enumerate(self.cell_buttons):
            for col, button in enumerate(row_buttons):
                product_number = BASE_NUMBER + row * 5 + col
                product = next(
                    (
                        product
                        for product in self.products_data
                        if product["number"] == product_number
                    ),
                    None,
                )

                if product:
                    image_path = f"assets/img/{product['image']}"
                else:
                    image_path = "assets/img/empty.png"

                img = Image.open(image_path)
                img.thumbnail((50, 50))
                img_tk = ImageTk.PhotoImage(img)
                button.config(
                    image=img_tk, text=product_number, compound=tk.TOP, bg="white"
                )
                button.image = img_tk

    def on_cell_click(self, row, col):
        product_number = BASE_NUMBER + row * 5 + col
        product = next(
            (
                product
                for product in self.products_data
                if product["number"] == product_number
            ),
            None,
        )

        # If another button was selected before, reset its appearance
        if self.previous_selected_button:
            self.previous_selected_button.config(relief=tk.RAISED, bg="white")

        # Mark the current button as selected
        current_button = self.cell_buttons[row][col]
        current_button.config(relief=tk.SUNKEN, bg="lightblue")

        # Store the current button as the previously selected one
        self.previous_selected_button = current_button

        if product:
            self.selected_product = product
            self.set_buttons_state()
        else:
            self.set_buttons_state(disabled=True)

    def set_buttons_state(self, disabled=False):
        state = tk.DISABLED if disabled else tk.NORMAL
        self.edit_button["state"] = state
        self.delete_button["state"] = state
        self.add_button["state"] = tk.NORMAL if disabled else tk.DISABLED

    def edit_product(self):
        if not self.selected_product:
            return

        # Assuming you have an instance of Inventory class named 'inventory'
        self.inventory = Inventory(self.products_data)

        # Creating new window for editing product details
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Product Details")
        edit_window.geometry("350x500")
        edit_window.configure(bg="#f4f4f4")  # Light gray background

        # Title
        title_label = tk.Label(
            edit_window, text="Edit Product", font=("Arial", 20, "bold"), bg="#f4f4f4"
        )
        title_label.pack(pady=20)

        # Display product image
        image_path = f"assets/img/{self.selected_product['image']}"
        img = Image.open(image_path)
        img.thumbnail((150, 150))
        img_tk = ImageTk.PhotoImage(img)
        label = tk.Label(edit_window, image=img_tk, bg="#f4f4f4")
        label.image = img_tk
        label.pack(pady=10)

        # Container frame for entries
        frame = tk.Frame(edit_window, bg="#f4f4f4")
        frame.pack(pady=10, padx=20)

        # Display & edit product details
        label_names = ["Name:", "Slot Number:", "Quantity:", "Price:"]
        details = [
            self.selected_product["name"],
            self.selected_product["number"],
            inventory.get_stock(self.selected_product["number"]),
            self.selected_product["price"],
        ]
        vars_list = []

        for i, label_name in enumerate(label_names):
            tk.Label(frame, text=label_name, bg="#f4f4f4", font=("Arial", 12)).grid(
                row=i, column=0, pady=5, sticky="w"
            )
            var = tk.StringVar(value=details[i])
            entry = tk.Entry(frame, textvariable=var, font=("Arial", 12))
            if label_name == "Slot Number:":
                entry.config(state="readonly")  # Slot Number is not editable
            entry.grid(row=i, column=1, pady=5)
            vars_list.append(var)

        # Save button to update details
        def save_changes():
            self.selected_product["name"] = vars_list[0].get()
            inventory.stock[self.selected_product["number"]] = int(vars_list[2].get())
            self.selected_product["price"] = vars_list[3].get()
            edit_window.destroy()
            self.update_cell_buttons()  # refresh to reflect changes

            if self.update_callback:
                self.update_callback()  # Notify the main app about the change

                # After saving the changes, refresh the main app's product display
            self.parent.refresh_product_display()

        save_button = tk.Button(
            edit_window,
            text="Save",
            command=save_changes,
            bg="#82c9a1",
            font=("Arial", 12),
            width=15,
        )
        save_button.pack(pady=20)

        edit_window.mainloop()

    def delete_product(self):
        if self.selected_product:
            print("Delete product:", self.selected_product)

    def add_product(self):
        if self.selected_product:
            print("Add product, selected number:", self.selected_product["number"])


class VendingMachineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vending Machine Simulator")
        self.geometry("650x840")  # Set a larger size for the main window
        self.resizable(False, False)

        self.copied_image_label = None  # Add this line to store the label reference

        # Call the method to set the background image
        self.set_background()

        # Create a list to store all the PhotoImage instances for the product images
        self.product_images = []

        # Create a dictionary to store the product number and its corresponding image
        self.product_images_dict = {}

        # Create a Products and inventory instance to access the product data
        self.products_data = Products()
        self.inventory = Inventory(self.products_data)

        # Initialize variables for coin input and user selection
        self.current_coins = 0.0
        self.selected_product = None
        self.selected_number = ""

        # Create a dictionary to store the quantity of each product
        self.product_quantities = {
            product["number"]: tk.IntVar()
            for product in self.products_data.get_products()
        }

        # Redraw the vending machine grid
        self.create_vending_grid()

        # Create the vending machine grid
        self.create_vending_grid()

        # Create the 'buy' button
        self.create_buy_button()

        # Create the numpad
        self.transaction = Transaction(self)
        self.create_numpad()

        # Variable to store the id of the scheduled countdown
        self.countdown_id = None

        # Create a set to store the product numbers present in the vending machine
        self.product_numbers = set(
            product["number"] for product in self.products_data.get_products()
        )

    def refresh_product_display(self):
        # Clear previous product display
        for widget in self.grid_slaves():
            widget.destroy()

        # Update product and inventory data
        self.products_data = Products()
        self.inventory = Inventory()
        self.product_quantities = {
            product["number"]: tk.IntVar()
            for product in self.products_data.get_products()
        }

    def set_background(self):
        # Load the image file
        bg_image = tk.PhotoImage(file="assets/img/background.png")

        # Create a label to display the background image and make it fill the entire window
        bg_label = tk.Label(self, image=bg_image)
        bg_label.place(x=-175, y=0, anchor="nw")

        # Make sure to keep a reference to the image, otherwise it will be garbage collected
        bg_label.image = bg_image

    def display_copied_image(self, product_number):
        # Get the PhotoImage object of the purchased product from the dictionary
        copied_img = self.product_images_dict[product_number]

        # If there is a previous copied image label, destroy it first
        if self.copied_image_label:
            self.copied_image_label.destroy()

        # Create a label to display the copied image at the bottom of the window
        self.copied_image_label = tk.Label(self, image=copied_img)
        self.copied_image_label.image = copied_img

        # Place the copied image label at the desired location at the bottom of the window
        self.copied_image_label.place(x=220, y=595)  # Adjust the coordinates as needed

        # Schedule the removal of the copied image after 3 seconds
        self.after(3000, self.remove_copied_image)

    def create_vending_grid(self):
        max_product_number = (
            BASE_NUMBER + 29
        )  # The maximum product number you want to display

        # Clear the existing widgets in the vending grid
        for widget in self.grid_slaves():
            widget.destroy()

        # Create a dictionary to store the product number and its corresponding image
        product_images_dict = {}

        for product in self.products_data.get_products():
            number = product["number"]
            image_path = f"assets/img/{product['image']}"

            if number <= max_product_number:
                name = product["name"]
                price = product["price"]

                if self.inventory.get_stock(number) > 0:
                    # Product is available, display the product image

                    # Open the image using Pillow
                    img_pil = Image.open(image_path)

                    # Calculate the downsampling factor to limit the dimensions to 50x50 pixels
                    img_pil.thumbnail((50, 50))

                    # Convert the Pillow image to ImageTk format for tkinter
                    img = ImageTk.PhotoImage(img_pil)

                    # Store the image in the dictionary
                    product_images_dict[number] = img

                    # Store the image in the dictionary with the product number as the key
                    self.product_images_dict[number] = img

                    # Append the PhotoImage instance to the product_images list
                    self.product_images.append(img)
                else:
                    # Product is out of stock, display the empty symbol image

                    empty_image_path = "assets/img/empty.png"
                    empty_img = Image.open(empty_image_path)
                    empty_img.thumbnail((50, 50))
                    img = ImageTk.PhotoImage(empty_img)

                    # Store the empty image in the dictionary
                    product_images_dict[number] = img

                    # Store the image in the dictionary with the product number as the key
                    self.product_images_dict[number] = img
            else:
                # Slot is out of range, display the empty symbol image

                empty_image_path = "assets/img/empty.png"
                empty_img = Image.open(empty_image_path)
                empty_img.thumbnail((50, 50))
                img = ImageTk.PhotoImage(empty_img)

                # Store the empty image in the dictionary
                product_images_dict[number] = img

                # Store the image in the dictionary with the product number as the key
                self.product_images_dict[number] = img

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
            info_label_number.place(x=col * 45 + 122, y=row * 73 + 175, anchor="center")

            # Create and display the product price label
            info_label = tk.Label(self, text=f"€{price:.2f}")
            info_label.grid(row=row + 1, column=col, padx=5, pady=5)
            info_label.place(x=col * 45 + 122, y=row * 73 + 190, anchor="center")

        # Continue with the remaining code for empty slot labels and other elements
        # ...

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
                empty_slot_label.grid(row=row + 1, column=col, padx=5, pady=5)
                empty_slot_label.place(
                    x=col * 45 + 123, y=row * 73 + 150, anchor="center"
                )

                # Create and display the product number label
                info_label_number = tk.Label(self, text=f"{number}")
                info_label_number.grid(row=row + 1, column=col, padx=5, pady=5)
                info_label_number.place(
                    x=col * 45 + 122, y=row * 73 + 175, anchor="center"
                )

    def remove_copied_image(self):
        if self.copied_image_label:
            self.copied_image_label.destroy()
            self.copied_image_label = None

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
        self.coin_amount_label = tk.Label(
            self, text="Current Coins: $0.00", font=("Arial", 12, "bold")
        )
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

    # Create the Products instance and pass it to the main app
    products_data = Products()

    def open_product_management():
        product_management_window = ProductManagementWindow(
            app, products_data.get_products()
        )
        product_management_window.grab_set()

    open_button = tk.Button(
        app, text="Open Product Management", command=open_product_management
    )
    open_button.pack()

    # working code

    app.mainloop()
