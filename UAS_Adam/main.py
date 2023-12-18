
from http import HTTPStatus
from flask import Flask, request, abort
from flask_restful import Resource, Api 
from models import Jeruk as JenisJeruk
from engine import engine
from sqlalchemy import select
from sqlalchemy.orm import Session

session = Session(engine)

app = Flask(__name__)
api = Api(app)        

class BaseMethod():

    def __init__(self):
        self.raw_weight = {'rasa': 9, 'kandungan_gula': 5, 'ukuran': 7, 'harga': 8, 'aroma': 5}

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k, v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(JenisJeruk.jenis_jeruk, JenisJeruk.rasa, JenisJeruk.kandungan_gula, JenisJeruk.ukuran, JenisJeruk.harga, JenisJeruk.aroma)
        result = session.execute(query).fetchall()
        print(result)
        return [{'jenis_jeruk': data_jeruk.jenis_jeruk, 'rasa': data_jeruk.rasa, 'kandungan_gula': data_jeruk.kandungan_gula, 'ukuran': data_jeruk.ukuran, 'harga': data_jeruk.harga, 'aroma': data_jeruk.aroma} for data_jeruk in result]

    @property
    def normalized_data(self):
        rasa_values= []
        kandungan_gula_values = []
        ukuran_values = []
        harga_values = []
        aroma_values = []

        for data in self.data:
            rasa_values.append(data['rasa'])
            kandungan_gula_values.append(data['kandungan_gula'])
            ukuran_values.append(data['ukuran'])
            harga_values.append(data['harga'])
            aroma_values.append(data['aroma'])

        return [
            {'jenis_jeruk': data['jenis_jeruk'],
             'rasa': data['rasa'] / max(rasa_values),
             'kandungan_gula': data['kandungan_gula'] / max(kandungan_gula_values),
             'ukuran': data['ukuran'] / max(ukuran_values),
             'harga': min(harga_values) / data['harga'],
             'aroma': data['aroma'] / max(aroma_values)
             }
            for data in self.data
        ]

    def update_weights(self, new_weights):
        self.raw_weight = new_weights

class WeightedProductCalculator(BaseMethod):
    def update_weights(self, new_weights):
        self.raw_weight = new_weights

    @property
    def calculate(self):
        normalized_data = self.normalized_data
        produk = []

        for row in normalized_data:
            product_score = (
                row['rasa'] ** self.raw_weight['rasa'] *
                row['kandungan_gula'] ** self.raw_weight['kandungan_gula'] *
                row['ukuran'] ** self.raw_weight['ukuran']*
                row['harga'] ** self.raw_weight['harga'] *
                row['aroma'] ** self.raw_weight['aroma'] 
            )

            produk.append({
                'jenis_jeruk': row['jenis_jeruk'],
                'produk': product_score
            })

        sorted_produk = sorted(produk, key=lambda x: x['produk'], reverse=True)

        sorted_data = []

        for product in sorted_produk:
            sorted_data.append({
                'jenis_jeruk': product['jenis_jeruk'],
                'score': product['produk']
            })

        return sorted_data


class WeightedProduct(Resource):
    def get(self):
        calculator = WeightedProductCalculator()
        result = calculator.calculate
        return result, HTTPStatus.OK.value
    
    def post(self):
        new_weights = request.get_json()
        calculator = WeightedProductCalculator()
        calculator.update_weights(new_weights)
        result = calculator.calculate
        return {'data': result}, HTTPStatus.OK.value
    

class SimpleAdditiveWeightingCalculator(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        result = {row['jenis_jeruk']:
                  round(row['rasa'] * weight['rasa'] +
                        row['kandungan_gula'] * weight['kandungan_gula'] +
                        row['ukuran'] * weight['ukuran'] +
                        row['harga'] * weight['harga'] +
                        row['aroma'] * weight['aroma'], 2)
                  for row in self.normalized_data
                  }
        sorted_result = dict(
            sorted(result.items(), key=lambda x: x[1], reverse=True))
        return sorted_result

    def update_weights(self, new_weights):
        self.raw_weight = new_weights

class SimpleAdditiveWeighting(Resource):
    def get(self):
        saw = SimpleAdditiveWeightingCalculator()
        result = saw.calculate
        return result, HTTPStatus.OK.value

    def post(self):
        new_weights = request.get_json()
        saw = SimpleAdditiveWeightingCalculator()
        saw.update_weights(new_weights)
        result = saw.calculate
        return {'data': result}, HTTPStatus.OK.value


class Jeruk(Resource):
    def get_paginated_result(self, url, list, args):
        page_size = int(args.get('page_size', 10))
        page = int(args.get('page', 1))
        page_count = int((len(list) + page_size - 1) / page_size)
        start = (page - 1) * page_size
        end = min(start + page_size, len(list))

        if page < page_count:
            next_page = f'{url}?page={page+1}&page_size={page_size}'
        else:
            next_page = None
        if page > 1:
            prev_page = f'{url}?page={page-1}&page_size={page_size}'
        else:
            prev_page = None
        
        if page > page_count or page < 1:
            abort(404, description=f'Halaman {page} tidak ditemukan.') 
        return {
            'page': page, 
            'page_size': page_size,
            'next': next_page, 
            'prev': prev_page,
            'Results': list[start:end]
        }

    def get(self):
        query = select(JenisJeruk)
        data = [{'jenis_jeruk': data_jeruk.jenis_jeruk, 'rasa': data_jeruk.rasa, 'kandungan_gula': data_jeruk.kandungan_gula, 'ukuran': data_jeruk.ukuran, 'harga': data_jeruk.harga, 'aroma': data_jeruk.aroma} for data_jeruk in session.scalars(query)]
        return self.get_paginated_result('data_jeruk/', data, request.args), HTTPStatus.OK.value


api.add_resource(Jeruk, '/data_jeruk')
api.add_resource(WeightedProduct, '/wp')
api.add_resource(SimpleAdditiveWeighting, '/saw')

if __name__ == '__main__':
    app.run(port='5005', debug=True)
