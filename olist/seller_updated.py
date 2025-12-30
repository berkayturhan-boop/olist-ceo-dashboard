from __future__ import annotations

from pathlib import Path
import pandas as pd
import numpy as np


class Seller:
    """
    CEO_request projesi için seller bazlı eğitim datası üretir.

    Bu revize versiyon, CSV'leri her bilgisayarda sorunsuz bulabilmek için
    proje kökündeki `data/` klasöründen Path ile okur.
    """

    def __init__(self, data_dir: str | Path | None = None):
        # Bu dosya: .../CEO_talebi_takim1/olist/seller_updated.py
        base_dir = Path(__file__).resolve().parent          # .../olist
        project_root = base_dir.parent                      # .../CEO_talebi_takim1

        self.data_dir = Path(data_dir) if data_dir else (project_root / "data")
        self.data = self._load_data()

    # -----------------------------
    # Load required CSVs (robust paths)
    # -----------------------------
    def _load_data(self) -> dict[str, pd.DataFrame]:
        """
        Projede kullandığımız minimum tablolar:
        - sellers
        - orders
        - order_items
        - order_reviews
        """
        required = {
            "sellers": "olist_sellers_dataset.csv",
            "orders": "olist_orders_dataset.csv",
            "order_items": "olist_order_items_dataset.csv",
            "order_reviews": "olist_order_reviews_dataset.csv",
        }

        missing = [fname for fname in required.values() if not (self.data_dir / fname).exists()]
        if missing:
            raise FileNotFoundError(
                "Gerekli CSV dosyaları bulunamadı.\n"
                f"Aranan klasör: {self.data_dir}\n"
                f"Eksik dosyalar: {missing}\n\n"
                "Çözüm: Bu CSV'leri repo kökündeki `data/` klasörüne koyup push'layın."
            )

        # Okuma (id kolonlarını string tutmak güvenli)
        sellers = pd.read_csv(self.data_dir / required["sellers"], dtype={"seller_id": "string"})
        orders = pd.read_csv(self.data_dir / required["orders"], dtype={"order_id": "string"})
        order_items = pd.read_csv(
            self.data_dir / required["order_items"],
            dtype={"order_id": "string", "seller_id": "string"},
        )
        order_reviews = pd.read_csv(
            self.data_dir / required["order_reviews"],
            dtype={"order_id": "string"},
        )

        return {
            "sellers": sellers,
            "orders": orders,
            "order_items": order_items,
            "order_reviews": order_reviews,
        }

    # -----------------------------
    # Basic seller features
    # -----------------------------
    def get_seller_features(self) -> pd.DataFrame:
        sellers = self.data["sellers"][["seller_id", "seller_city", "seller_state"]].drop_duplicates()
        return sellers

    # -----------------------------
    # Delay to carrier & wait time (delivered orders only)
    # -----------------------------
    def get_seller_delay_wait_time(self) -> pd.DataFrame:
        order_items = self.data["order_items"][["order_id", "seller_id", "shipping_limit_date"]].copy()
        orders = self.data["orders"][
            [
                "order_id",
                "order_status",
                "order_purchase_timestamp",
                "order_delivered_carrier_date",
                "order_delivered_customer_date",
            ]
        ].copy()

        # Only delivered orders (otherwise dates can be NaT)
        orders = orders.query("order_status == 'delivered'").copy()

        ship = order_items.merge(orders, on="order_id", how="inner")

        # Datetimes
        for col in [
            "shipping_limit_date",
            "order_purchase_timestamp",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
        ]:
            ship[col] = pd.to_datetime(ship[col], errors="coerce")

        # Per row durations (days as float)
        ship["delay_to_carrier_days"] = (
            (ship["order_delivered_carrier_date"] - ship["shipping_limit_date"]) / np.timedelta64(1, "D")
        )
        ship["delay_to_carrier_days"] = ship["delay_to_carrier_days"].clip(lower=0)

        ship["wait_time_days"] = (
            (ship["order_delivered_customer_date"] - ship["order_purchase_timestamp"]) / np.timedelta64(1, "D")
        )

        # Aggregate per seller
        out = ship.groupby("seller_id", as_index=False).agg(
            delay_to_carrier=("delay_to_carrier_days", "mean"),
            wait_time=("wait_time_days", "mean"),
        )

        return out

    # -----------------------------
    # Active dates
    # -----------------------------
    def get_active_dates(self) -> pd.DataFrame:
        orders = self.data["orders"][["order_id", "order_approved_at"]].dropna().copy()
        order_items = self.data["order_items"][["order_id", "seller_id"]].drop_duplicates()

        orders_sellers = order_items.merge(orders, on="order_id", how="inner")
        orders_sellers["order_approved_at"] = pd.to_datetime(orders_sellers["order_approved_at"], errors="coerce")

        dates = orders_sellers.groupby("seller_id", as_index=False).agg(
            date_first_sale=("order_approved_at", "min"),
            date_last_sale=("order_approved_at", "max"),
        )

        dates["months_on_olist"] = (
            (dates["date_last_sale"] - dates["date_first_sale"]) / np.timedelta64(30, "D")
        ).round()

        return dates

    # -----------------------------
    # Quantity + number of orders
    # -----------------------------
    def get_quantity(self) -> pd.DataFrame:
        order_items = self.data["order_items"][["order_id", "seller_id"]].copy()

        n_orders = order_items.groupby("seller_id", as_index=False)["order_id"].nunique()
        n_orders = n_orders.rename(columns={"order_id": "n_orders"})

        quantity = order_items.groupby("seller_id", as_index=False)["order_id"].count()
        quantity = quantity.rename(columns={"order_id": "quantity"})

        out = n_orders.merge(quantity, on="seller_id", how="inner")
        out["quantity_per_order"] = out["quantity"] / out["n_orders"]

        return out

    # -----------------------------
    # Sales (sum of item prices)
    # -----------------------------
    def get_sales(self) -> pd.DataFrame:
        order_items = self.data["order_items"][["seller_id", "price"]].copy()
        sales = order_items.groupby("seller_id", as_index=False)["price"].sum()
        sales = sales.rename(columns={"price": "sales"})
        return sales

    # -----------------------------
    # Reviews: mean score + shares + cost_of_reviews
    # -----------------------------
    def get_review_score(self) -> pd.DataFrame:
        order_items = self.data["order_items"][["order_id", "seller_id"]].drop_duplicates()
        reviews = self.data["order_reviews"][["order_id", "review_score"]].copy()

        merged = order_items.merge(reviews, on="order_id", how="inner")
        merged = merged.dropna(subset=["review_score"]).copy()

        merged["review_score"] = merged["review_score"].astype(float)

        # Shares
        merged["dim_is_one_star"] = (merged["review_score"] == 1).astype(int)
        merged["dim_is_five_star"] = (merged["review_score"] == 5).astype(int)

        # Cost mapping: 1★=100, 2★=50, 3★=40, 4★=0, 5★=0
        cost_map = {1: 100, 2: 50, 3: 40, 4: 0, 5: 0}
        merged["review_cost"] = merged["review_score"].map(cost_map).fillna(0)

        out = merged.groupby("seller_id", as_index=False).agg(
            share_of_one_stars=("dim_is_one_star", "mean"),
            share_of_five_stars=("dim_is_five_star", "mean"),
            review_score=("review_score", "mean"),
            cost_of_reviews=("review_cost", "sum"),
        )

        return out

    # -----------------------------
    # Final training set (CEO_request version)
    # -----------------------------
    def get_training_data(self) -> pd.DataFrame:
        base = (
            self.get_seller_features()
            .merge(self.get_seller_delay_wait_time(), on="seller_id", how="inner")
            .merge(self.get_active_dates(), on="seller_id", how="inner")
            .merge(self.get_quantity(), on="seller_id", how="inner")
            .merge(self.get_sales(), on="seller_id", how="inner")
        )

        reviews = self.get_review_score()
        df = base.merge(reviews, on="seller_id", how="inner")

        # Revenues: 10% commission on sales + 80 BRL/month subscription
        df["revenues"] = 0.1 * df["sales"] + 80 * df["months_on_olist"]

        # Profits (gross, before IT operational costs)
        df["profits"] = df["revenues"] - df["cost_of_reviews"]

        keep_cols = [
            "seller_id",
            "seller_city",
            "seller_state",
            "delay_to_carrier",
            "wait_time",
            "date_first_sale",
            "date_last_sale",
            "months_on_olist",
            "n_orders",
            "quantity",
            "quantity_per_order",
            "sales",
            "share_of_one_stars",
            "share_of_five_stars",
            "review_score",
            "cost_of_reviews",
            "revenues",
            "profits",
        ]
        return df[keep_cols]
