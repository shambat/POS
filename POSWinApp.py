import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime

class POSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SHAM POS System")

        # Set initial window size and position
        self.window_width = 800
        self.window_height = 600
        self.root.geometry(f"{self.window_width}x{self.window_height}+100+100")

        # Color Scheme
        self.bg_color = "#f5f5f5"  # Light gray background
        self.primary_color = "#3498db"  # Blue accent
        self.secondary_color = "#2c3e50"  # Dark gray for text and headers
        self.button_bg_color = "#2980b9"  # Button color
        self.button_hover_bg_color = "#1e6a8a"  # Button hover color
        self.button_text_color = "#ffffff"  # Button text color

        # Title Label
        self.title_label = tk.Label(self.root, text="SHAM POS System", font=("Arial", 20, "bold"), bg=self.bg_color, fg=self.secondary_color)
        self.title_label.pack(fill=tk.X, pady=10)

        # Control Buttons Frame
        self.control_frame = tk.Frame(self.root, bg=self.bg_color)
        self.control_frame.pack(pady=10)

        self.fullscreen_button = tk.Button(self.control_frame, text="Fullscreen", command=self.toggle_fullscreen, bg=self.button_bg_color, fg=self.button_text_color, font=("Arial", 12), activebackground=self.button_hover_bg_color, relief="raised", padx=5, pady=3)
        self.fullscreen_button.pack(side=tk.LEFT, padx=5)
        
        self.windowed_button = tk.Button(self.control_frame, text="Windowed", command=self.toggle_windowed, bg=self.button_bg_color, fg=self.button_text_color, font=("Arial", 12), activebackground=self.button_hover_bg_color, relief="raised", padx=5, pady=3)
        self.windowed_button.pack(side=tk.LEFT, padx=5)
        
        self.quit_button = tk.Button(self.control_frame, text="Quit", command=self.quit_app, bg="#e74c3c", fg=self.button_text_color, font=("Arial", 12), activebackground="#c0392b", relief="raised", padx=5, pady=3)
        self.quit_button.pack(side=tk.LEFT, padx=5)

        # Product Entry Frame
        self.product_frame = tk.Frame(self.root, bg=self.bg_color)
        self.product_frame.pack(pady=10)

        tk.Label(self.product_frame, text="Product Name:", bg=self.bg_color, fg=self.secondary_color, font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.product_name = tk.Entry(self.product_frame, font=("Arial", 12), bg="#ffffff", fg=self.secondary_color, borderwidth=1, relief="solid")
        self.product_name.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(self.product_frame, text="Quantity:", bg=self.bg_color, fg=self.secondary_color, font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.quantity = tk.Entry(self.product_frame, font=("Arial", 12), bg="#ffffff", fg=self.secondary_color, borderwidth=1, relief="solid")
        self.quantity.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(self.product_frame, text="Price:", bg=self.bg_color, fg=self.secondary_color, font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.price = tk.Entry(self.product_frame, font=("Arial", 12), bg="#ffffff", fg=self.secondary_color, borderwidth=1, relief="solid")
        self.price.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        self.add_button = tk.Button(self.product_frame, text="Add to Cart", command=self.add_to_cart, bg=self.button_bg_color, fg=self.button_text_color, font=("Arial", 12), activebackground=self.button_hover_bg_color, relief="raised", padx=10, pady=5)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Cart Frame
        self.cart_frame = tk.Frame(self.root, bg=self.bg_color)
        self.cart_frame.pack(pady=10)

        self.cart_listbox = tk.Listbox(self.cart_frame, width=80, height=10, font=("Arial", 10), bg="#ffffff", fg=self.secondary_color, borderwidth=1, relief="solid")
        self.cart_listbox.pack()

        # Checkout Frame
        self.checkout_frame = tk.Frame(self.root, bg=self.bg_color)
        self.checkout_frame.pack(pady=10)

        self.total_label = tk.Label(self.checkout_frame, text="Total: $0", font=("Arial", 16, "bold"), bg=self.bg_color, fg=self.secondary_color)
        self.total_label.pack(side=tk.LEFT, padx=10)

        self.checkout_button = tk.Button(self.checkout_frame, text="Checkout", command=self.checkout, bg=self.button_bg_color, fg=self.button_text_color, font=("Arial", 12), activebackground=self.button_hover_bg_color, relief="raised", padx=10, pady=5)
        self.checkout_button.pack(side=tk.LEFT)

        # Initialize cart
        self.cart = []

    def toggle_fullscreen(self):
        self.root.attributes('-fullscreen', True)
        self.fullscreen_button.config(bg=self.button_hover_bg_color)
        self.windowed_button.config(bg=self.button_bg_color)
        self.quit_button.config(bg=self.button_bg_color)
        self.root.bind("<Escape>", self.exit_fullscreen)  # Bind Escape key to exit fullscreen

    def toggle_windowed(self):
        self.root.attributes('-fullscreen', False)
        self.root.geometry(f"{self.window_width}x{self.window_height}+100+100")
        self.fullscreen_button.config(bg=self.button_bg_color)
        self.windowed_button.config(bg=self.button_hover_bg_color)
        self.quit_button.config(bg=self.button_bg_color)
        self.root.unbind("<Escape>")  # Unbind Escape key when in windowed mode

    def exit_fullscreen(self, event=None):
        self.toggle_windowed()  # Switch back to windowed mode

    def add_to_cart(self):
        name = self.product_name.get()
        quantity = self.quantity.get()
        price = self.price.get()

        if name and quantity and price:
            try:
                total_price = int(quantity) * float(price)
                self.cart.append((name, quantity, price, total_price))
                self.cart_listbox.insert(tk.END, f"{name} - {quantity} @ ${price} each = ${total_price:.2f}")
                self.update_total()
                self.clear_entries()
            except ValueError:
                messagebox.showwarning("Input Error", "Quantity and Price must be numbers")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")

    def update_total(self):
        total = sum(item[3] for item in self.cart)
        self.total_label.config(text=f"Total: ${total:.2f}")

    def checkout(self):
        if self.cart:
            total_amount = sum(item[3] for item in self.cart)
            purchase_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save record to CSV
            self.save_to_csv(purchase_time, total_amount)

            messagebox.showinfo("Checkout", f"Total Amount Due: ${total_amount:.2f}")
            self.cart.clear()
            self.cart_listbox.delete(0, tk.END)
            self.update_total()
        else:
            messagebox.showwarning("Cart Empty", "There are no items in the cart.")

    def save_to_csv(self, purchase_time, amount):
        with open('purchase_records.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([purchase_time, amount])

    def clear_entries(self):
        self.product_name.delete(0, tk.END)
        self.quantity.delete(0, tk.END)
        self.price.delete(0, tk.END)

    def quit_app(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = POSApp(root)
    root.mainloop()
