# orders/management/commands/populate_data.py
from django.core.management.base import BaseCommand
from Order_Dashboard.models import (
    Color, Party_Master, Sub_Party_Master,
    Product_Master, Orders, OrderItem
)


class Command(BaseCommand):
    help = "Populates the database with sample shoe order data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting data population...\n")
        self._clear_existing_data()
        colors      = self._populate_colors()
        parties     = self._populate_parties()
        sub_parties = self._populate_sub_parties(parties)
        products    = self._populate_products(colors)
        self._populate_orders(parties, sub_parties, products, colors)
        self.stdout.write(self.style.SUCCESS("\nData population complete!"))

    # ── Step 0 : Clear Existing Data ───────────────────────────────
    def _clear_existing_data(self):
        self.stdout.write("Clearing existing data...")
        OrderItem.objects.all().delete()
        Orders.objects.all().delete()
        Product_Master.objects.all().delete()
        Sub_Party_Master.objects.all().delete()
        Party_Master.objects.all().delete()
        Color.objects.all().delete()
        self.stdout.write(self.style.WARNING("  Existing data cleared."))

    # ── Step 1 : Colors ────────────────────────────────────────────
    def _populate_colors(self):
        self.stdout.write("Creating colors...")
        color_names = ["Red", "Blue", "Black", "White", "Brown",
                       "Green", "Navy", "Grey", "Beige", "Pink"]
        colors = {}
        for name in color_names:
            obj, created = Color.objects.get_or_create(name=name)
            colors[name] = obj
            self.stdout.write(f"  [{'Created' if created else 'Exists'}] {name}")
        return colors

    # ── Step 2 : Parties ───────────────────────────────────────────
    def _populate_parties(self):
        self.stdout.write("Creating parties...")
        party_data = [
            {
                "name":            "Raj Footwear",
                "whatsapp_number": "9876543210",    # mandatory
                "transport":       "DTDC",
                "marka":           "RF",
                "station":         "Mumbai",
            },
            {
                "name":            "Mumbai Shoes Co",
                "whatsapp_number": "9123456780",    # mandatory
                "transport":       "FedEx",
                "marka":           "MSC",
                "station":         "Dadar",
            },
            {
                "name":            "Delhi Traders",
                "whatsapp_number": "9988776655",    # mandatory
                "transport":       "Delhivery",
                "marka":           "DT",
                "station":         "Karol Bagh",
            },
        ]
        parties = {}
        for data in party_data:
            obj, created         = Party_Master.objects.get_or_create(
                                       name=data["name"], defaults=data)
            parties[data["name"]] = obj
            self.stdout.write(
                f"  [{'Created' if created else 'Exists'}] "
                f"{obj.name} | WhatsApp: {obj.whatsapp_number}"
            )
        return parties

    # ── Step 3 : Sub Parties ───────────────────────────────────────
    def _populate_sub_parties(self, parties):
        self.stdout.write("Creating sub-parties...")
        sub_party_data = [
            {
                "name":         "Raj - Andheri",
                "parent_party": parties["Raj Footwear"],
                "transport":    "DTDC",
                "marka":        "RF-AND",
                "station":      "Andheri",
            },
            {
                "name":         "Raj - Bandra",
                "parent_party": parties["Raj Footwear"],
                "transport":    "BlueDart",
                "marka":        "RF-BAN",
                "station":      "Bandra",
            },
            {
                "name":         "Mumbai - Dadar",
                "parent_party": parties["Mumbai Shoes Co"],
                "transport":    "FedEx",
                "marka":        "MSC-DAD",
                "station":      "Dadar",
            },
            {
                "name":         "Delhi - Karol Bagh",
                "parent_party": parties["Delhi Traders"],
                "transport":    "Delhivery",
                "marka":        "DT-KB",
                "station":      "Karol Bagh",
            },
        ]
        sub_parties = {}
        for data in sub_party_data:
            obj, created              = Sub_Party_Master.objects.get_or_create(
                                            name=data["name"], defaults=data)
            sub_parties[data["name"]] = obj
            self.stdout.write(f"  [{'Created' if created else 'Exists'}] {obj.name}")
        return sub_parties

    # ── Step 4 : Products ──────────────────────────────────────────
    def _populate_products(self, colors):
        self.stdout.write("Creating products...")
        product_data = [
            {
                "name":            "Nike Air Force",
                "size_min":        6,
                "size_max":        11,
                "packing":         "box",
                "opening_balance": 100,
                "colors":          ["Red", "White", "Black"],
            },
            {
                "name":            "Adidas Superstar",
                "size_min":        5,
                "size_max":        10,
                "packing":         "box",
                "opening_balance": 80,
                "colors":          ["Black", "White", "Navy"],
            },
            {
                "name":            "Puma Sliders",
                "size_min":        4,
                "size_max":        9,
                "packing":         "loose",
                "opening_balance": 200,
                "colors":          ["Blue", "Black", "Grey"],
            },
            {
                "name":            "Bata Formal",
                "size_min":        6,
                "size_max":        11,
                "packing":         "china",
                "opening_balance": 60,
                "colors":          ["Black", "Brown"],
            },
        ]
        products = {}
        for data in product_data:
            product_colors = data.pop("colors")
            obj, created   = Product_Master.objects.get_or_create(
                                 name=data["name"], defaults=data)
            obj.color.set([colors[c] for c in product_colors])
            products[data["name"]] = obj
            self.stdout.write(
                f"  [{'Created' if created else 'Exists'}] {obj.name} "
                f"| Sizes: {obj.size_min}-{obj.size_max} "
                f"| Colors: {product_colors}"
            )
        return products

    # ── Step 5 : Orders + Items ────────────────────────────────────
    # ── Step 5 : Orders + Items ────────────────────────────────────
    def _populate_orders(self, parties, sub_parties, products, colors):
        self.stdout.write("Creating orders...")
        order_data = [
            {
                "party":     parties["Raj Footwear"],
                "sub_party": sub_parties["Raj - Andheri"],  # ← has sub-party
                "transport": "DTDC",
                "marka":     "RF-AND-001",
                "items": [
                    {
                        "product":  products["Nike Air Force"],
                        "quantity": 50,
                        "size_min": 7,
                        "size_max": 10,
                        "packing":  "box",
                        "colors":   ["Red", "White"],
                    },
                    {
                        "product":  products["Adidas Superstar"],
                        "quantity": 30,
                        "size_min": 6,
                        "size_max": 9,
                        "packing":  "box",
                        "colors":   ["Black"],
                    },
                ],
            },
            {
                "party":     parties["Raj Footwear"],
                "sub_party": None,                          # ← no sub-party (direct order)
                "transport": "BlueDart",
                "marka":     "RF-001",
                "items": [
                    {
                        "product":  products["Puma Sliders"],
                        "quantity": 20,
                        "size_min": 6,
                        "size_max": 9,
                        "packing":  "loose",
                        "colors":   ["Black"],
                    },
                ],
            },
            {
                "party":     parties["Mumbai Shoes Co"],
                "sub_party": sub_parties["Mumbai - Dadar"],  # ← has sub-party
                "transport": "FedEx",
                "marka":     "MSC-DAD-001",
                "items": [
                    {
                        "product":  products["Puma Sliders"],
                        "quantity": 100,
                        "size_min": 5,
                        "size_max": 8,
                        "packing":  "loose",
                        "colors":   ["Blue", "Grey"],
                    },
                ],
            },
            {
                "party":     parties["Mumbai Shoes Co"],
                "sub_party": None,                          # ← no sub-party (direct order)
                "transport": "FedEx",
                "marka":     "MSC-001",
                "items": [
                    {
                        "product":  products["Nike Air Force"],
                        "quantity": 40,
                        "size_min": 6,
                        "size_max": 10,
                        "packing":  "box",
                        "colors":   ["White", "Black"],
                    },
                ],
            },
            {
                "party":     parties["Delhi Traders"],
                "sub_party": sub_parties["Delhi - Karol Bagh"],  # ← has sub-party
                "transport": "Delhivery",
                "marka":     "DT-KB-001",
                "items": [
                    {
                        "product":  products["Bata Formal"],
                        "quantity": 25,
                        "size_min": 7,
                        "size_max": 11,
                        "packing":  "china",
                        "colors":   ["Black", "Brown"],
                    },
                ],
            },
        ]

        for data in order_data:
            items_data = data.pop("items")
            order      = Orders.objects.create(**data)

            sub_party_label = order.sub_party.name if order.sub_party else "Direct"
            self.stdout.write(
                f"  [Created] Order #{order.id} "
                f"| Party: {order.party.name} "
                f"| Sub-Party: {sub_party_label} "
                f"| Marka: {order.marka}"
            )

            for item in items_data:
                item_colors = item.pop("colors")
                order_item  = OrderItem.objects.create(order=order, **item)
                order_item.color.set([colors[c] for c in item_colors])
                self.stdout.write(
                    f"    → {order_item.product.name} "
                    f"| Qty: {order_item.quantity} "
                    f"| Sizes: {order_item.size_min}-{order_item.size_max} "
                    f"| Colors: {item_colors}"
                )