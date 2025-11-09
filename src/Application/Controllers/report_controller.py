from flask import request, jsonify, make_response, current_app
from src.Application.Service.report_service import ReportService

class ReportController:

    @staticmethod
    def get_top_3_products(id_usuario):
        return make_response(jsonify(ReportService.get_top_3_products(id_usuario)))
    

    @staticmethod
    def get_top_all_products(id_usuario):
        return make_response(jsonify(ReportService.get_all_products(id_usuario)))
    

    @staticmethod
    def get_specific_product(id_usuario, id_produto):
        return make_response(jsonify(ReportService.get_specific_product(id_usuario, id_produto)))

