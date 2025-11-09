from src.Config.db import db
from src.Infrastructure.Model.Sell_model import SellModel
from src.Infrastructure.Model.Product_model import ProductModel
from src.Infrastructure.Model.User_model import UserModel
from src.Domain.Sell import SellDomain
from sqlalchemy import func, desc


class ReportService:

    @staticmethod
    def get_top_3_products(id_usuario):
        top_products = (
            db.session.query(
                ProductModel.name.label('product_name'),
                func.sum(SellModel.quantity).label('total_vendido')
            )
            .join(ProductModel, ProductModel.id == SellModel.id_product)
            .filter(SellModel.id_seller == id_usuario)
            .group_by(ProductModel.id)
            .order_by(desc(func.sum(SellModel.quantity)))
            .limit(3)
            .all()
        )

        return [
            {"produto": p.product_name, "quantidade_vendida": p.total_vendido}
            for p in top_products
        ]



    @staticmethod
    def get_all_products(id_usuario):
        top_products = (
            db.session.query(
                ProductModel.name.label('product_name'),
                func.sum(SellModel.quantity).label('total_vendido')
            )
            .join(ProductModel, ProductModel.id == SellModel.id_product)
            .filter(SellModel.id_seller == id_usuario)
            .group_by(ProductModel.id)
            .order_by(desc(func.sum(SellModel.quantity)))
            .all()
        )

        return [
            {"produto": p.product_name, "quantidade_vendida": p.total_vendido}
            for p in top_products
        ]


    @staticmethod
    def get_specific_product(id_usuario, id_produto):
        top_products = (
            db.session.query(
                ProductModel.name.label('product_name'),
                func.sum(SellModel.quantity).label('total_vendido')
            )
            .join(ProductModel, ProductModel.id == SellModel.id_product)
            .filter(
                SellModel.id_seller == id_usuario,
                SellModel.id_product == id_produto
                    )
            .group_by(ProductModel.id)
            .order_by(desc(func.sum(SellModel.quantity)))
            .all()
        )

        return [
            {"produto": p.product_name, "quantidade_vendida": p.total_vendido}
            for p in top_products
        ]
