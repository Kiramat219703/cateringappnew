"""
Raham Jan Tent & Karakri Service
FINAL PROFESSIONAL VERSION
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from datetime import datetime
import os

# ---------------- WINDOW ----------------

Window.clearcolor = get_color_from_hex("#121212")

# ---------------- COLORS ----------------

BG = get_color_from_hex("#121212")
CARD = get_color_from_hex("#1E1E1E")
PRIMARY = get_color_from_hex("#FF9800")
WHITE = get_color_from_hex("#FFFFFF")
GRAY = get_color_from_hex("#BDBDBD")
GREEN = get_color_from_hex("#4CAF50")
RED = get_color_from_hex("#F44336")

# ---------------- STORAGE ----------------

store = JsonStore("inventory.json")

# ---------------- BUTTON ----------------

class CustomButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_color = PRIMARY
        self.color = WHITE
        self.bold = True
        self.font_size = "16sp"

# ---------------- CARD ----------------

class Card(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(rgba=CARD)

            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[20]
            )

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)

    def update_rect(self, *args):

        self.rect.pos = self.pos
        self.rect.size = self.size

# ---------------- MAIN SCREEN ----------------

class MainScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.inventory = []
        self.cart = []

        main = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        # ---------- HEADER ----------

        header = Card(
            orientation="vertical",
            size_hint_y=None,
            height=dp(220),
            padding=dp(10)
        )

        logo = Image(
            source="logo.png",
            allow_stretch=True
        )

        title = Label(
            text="Raham Jan Tent & Karakri Service",
            color=WHITE,
            font_size="22sp",
            bold=True
        )

        header.add_widget(logo)
        header.add_widget(title)

        main.add_widget(header)

        # ---------- INVENTORY ----------

        self.scroll = ScrollView()

        self.grid = GridLayout(
            cols=1,
            spacing=dp(10),
            size_hint_y=None,
            padding=dp(5)
        )

        self.grid.bind(
            minimum_height=self.grid.setter("height")
        )

        self.scroll.add_widget(self.grid)

        main.add_widget(self.scroll)

        # ---------- BUTTONS ----------

        btn_layout = BoxLayout(
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10)
        )

        add_btn = CustomButton(text="Add Item")
        add_btn.bind(on_press=self.show_add_popup)

        cart_btn = CustomButton(text="Cart")
        cart_btn.bind(on_press=self.show_cart)

        btn_layout.add_widget(add_btn)
        btn_layout.add_widget(cart_btn)

        main.add_widget(btn_layout)

        self.add_widget(main)

        self.load_inventory()

    # ---------- LOAD ----------

    def load_inventory(self):

        if store.exists("items"):
            self.inventory = store.get("items")["data"]

        self.refresh_inventory()

    # ---------- SAVE ----------

    def save_inventory(self):

        store.put("items", data=self.inventory)

    # ---------- REFRESH ----------

    def refresh_inventory(self):

        self.grid.clear_widgets()

        for item in self.inventory:

            card = Card(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(140),
                padding=dp(10),
                spacing=dp(10)
            )

            # FIX: Use logo.png if the item's image file does not exist
            img_source = item["image"] if os.path.exists(item["image"]) else "logo.png"
            img = Image(
                source=img_source,
                size_hint_x=None,
                width=dp(110)
            )

            details = BoxLayout(
                orientation="vertical",
                spacing=dp(5)
            )

            name = Label(
                text=item["name"],
                color=WHITE,
                bold=True,
                font_size="18sp"
            )

            price = Label(
                text=f"Rent: Rs {item['price']}",
                color=GRAY
            )

            add_btn = CustomButton(
                text="Add To Cart",
                size_hint_y=None,
                height=dp(45)
            )

            add_btn.bind(
                on_press=lambda x, i=item: self.quantity_popup(i)
            )

            details.add_widget(name)
            details.add_widget(price)
            details.add_widget(add_btn)

            card.add_widget(img)
            card.add_widget(details)

            self.grid.add_widget(card)

    # ---------- ADD ITEM ----------

    def show_add_popup(self, instance):

        layout = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(20)
        )

        name = TextInput(
            hint_text="Item Name",
            multiline=False
        )

        price = TextInput(
            hint_text="Price",
            multiline=False,
            input_filter="float"
        )

        image = TextInput(
            hint_text="Image Path (example chair.jpg)",
            multiline=False
        )

        save_btn = CustomButton(text="Save Item")

        layout.add_widget(name)
        layout.add_widget(price)
        layout.add_widget(image)
        layout.add_widget(save_btn)

        popup = Popup(
            title="Add Inventory Item",
            content=layout,
            size_hint=(0.9, 0.7)
        )

        def save_item(instance):
            # If user leaves image field empty, default to logo.png
            img_val = image.text.strip()
            if not img_val:
                img_val = "logo.png"

            self.inventory.append({
                "name": name.text,
                "price": price.text,
                "image": img_val
            })

            self.save_inventory()
            self.refresh_inventory()

            popup.dismiss()

        save_btn.bind(on_press=save_item)

        popup.open()

    # ---------- QUANTITY ----------

    def quantity_popup(self, item):

        layout = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(20)
        )

        qty = TextInput(
            text="1",
            multiline=False,
            input_filter="int"
        )

        days = TextInput(
            text="1",
            multiline=False,
            input_filter="int"
        )

        add_btn = CustomButton(text="Add")

        layout.add_widget(Label(
            text="Quantity",
            color=WHITE
        ))

        layout.add_widget(qty)

        layout.add_widget(Label(
            text="Days",
            color=WHITE
        ))

        layout.add_widget(days)

        layout.add_widget(add_btn)

        popup = Popup(
            title=item["name"],
            content=layout,
            size_hint=(0.8, 0.6)
        )

        def add_to_cart(instance):

            total = (
                float(item["price"])
                * int(qty.text)
                * int(days.text)
            )

            self.cart.append({
                "name": item["name"],
                "qty": qty.text,
                "days": days.text,
                "price": item["price"],
                "total": total
            })

            popup.dismiss()

        add_btn.bind(on_press=add_to_cart)

        popup.open()

    # ---------- CART ----------

    def show_cart(self, instance):

        layout = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(10)
        )

        scroll = ScrollView()

        grid = GridLayout(
            cols=1,
            spacing=dp(10),
            size_hint_y=None
        )

        grid.bind(
            minimum_height=grid.setter("height")
        )

        total_bill = 0

        for item in self.cart:

            total_bill += item["total"]

            card = Card(
                orientation="vertical",
                size_hint_y=None,
                height=dp(110),
                padding=dp(10)
            )

            card.add_widget(Label(
                text=item["name"],
                color=WHITE,
                bold=True
            ))

            card.add_widget(Label(
                text=f"{item['qty']} x {item['days']} days",
                color=GRAY
            ))

            card.add_widget(Label(
                text=f"Rs {item['total']}",
                color=PRIMARY
            ))

            grid.add_widget(card)

        scroll.add_widget(grid)

        layout.add_widget(scroll)

        total_label = Label(
            text=f"TOTAL: Rs {total_bill}",
            color=GREEN,
            bold=True,
            font_size="22sp",
            size_hint_y=None,
            height=dp(50)
        )

        layout.add_widget(total_label)

        receipt_btn = CustomButton(
            text="Generate Receipt",
            size_hint_y=None,
            height=dp(50)
        )

        receipt_btn.bind(
            on_press=lambda x: self.customer_popup(total_bill)
        )

        layout.add_widget(receipt_btn)

        popup = Popup(
            title="Cart",
            content=layout,
            size_hint=(0.95, 0.95)
        )

        popup.open()

    # ---------- CUSTOMER ----------

    def customer_popup(self, total_bill):

        layout = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(20)
        )

        customer = TextInput(
            hint_text="Customer Name",
            multiline=False
        )

        phone = TextInput(
            hint_text="Phone Number",
            multiline=False
        )

        demand = TextInput(
            hint_text="Demand Date",
            multiline=False
        )

        return_date = TextInput(
            hint_text="Return Date",
            multiline=False
        )

        payment = Spinner(
            text="Pending",
            values=("Paid", "Pending", "Partially Paid")
        )

        generate_btn = CustomButton(
            text="Save Receipt"
        )

        layout.add_widget(customer)
        layout.add_widget(phone)
        layout.add_widget(demand)
        layout.add_widget(return_date)
        layout.add_widget(payment)
        layout.add_widget(generate_btn)

        popup = Popup(
            title="Customer Details",
            content=layout,
            size_hint=(0.9, 0.9)
        )

        def save_receipt(instance):

            text = f"""
Raham Jan Tent & Karakri Service

Customer: {customer.text}
Phone: {phone.text}

Demand Date: {demand.text}
Return Date: {return_date.text}

Payment: {payment.text}

-----------------------------
"""

            for item in self.cart:

                text += f"""

Item: {item['name']}
Qty: {item['qty']}
Days: {item['days']}
Total: Rs {item['total']}
"""

            text += f"""

-----------------------------

TOTAL BILL: Rs {total_bill}

Generated:
{datetime.now()}

"""

            filename = f"Receipt_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"

            # On Android, this saves to app's internal storage (no permission needed)
            path = os.path.join(os.getcwd(), filename)

            with open(path, "w", encoding="utf-8") as file:
                file.write(text)

            success = Popup(
                title="Success",
                content=Label(
                    text=f"Receipt Saved\n{filename}\n(in app storage)",
                    color=WHITE
                ),
                size_hint=(0.8, 0.4)
            )

            success.open()

            self.cart.clear()

            popup.dismiss()

        generate_btn.bind(on_press=save_receipt)

        popup.open()

# ---------------- APP ----------------

class CateringApp(App):

    def build(self):

        sm = ScreenManager()

        sm.add_widget(
            MainScreen(name="main")
        )

        return sm

# ---------------- RUN ----------------

if __name__ == "__main__":
    CateringApp().run()