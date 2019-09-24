from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import csv

app = Flask(__name__)
api = Api(app)


class HealthCehck(Resource):
    def get(self):
        return {'message': 'alive', 'hello': 'tina'}

    def post(self):
        self.get()


class FindBook(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        utterance = json_data['userRequest']['utterance']
        book_result = find_book_by_name(utterance)
        chat_bubbles = []
        if len(book_result):
            for b in book_result:
                chat_bubbles.append({
                    "simpleText": {
                        "text": '위치 : %s\n'
                                '도서명 : %s\n'
                                '저자 : %s\n'
                                '출판사 : %s\n' %
                                (b[0], b[1], b[2], b[3])
                    }
                })
        else:
            chat_bubbles.append({
                    "simpleText": {
                        "text": '찾으시는 도서는 라이브러리에 없어요. (감동)'
                    }
                })

        return {
            "version": "2.0",
            "template": {
                "outputs": chat_bubbles
            }
        }


api.add_resource(HealthCehck, '/', '/health_check')
api.add_resource(FindBook, '/find-book')

with open('./books.csv', 'r') as f:
    rdr = csv.reader(f)
    books = [a for a in rdr]
    books = books[1:]


def find_book_by_name(name):
    # category,book_name,author,publisher
    result = []
    name = name.replace(' ', '')
    for b in books:
        for b_i in b[1:3]:
            b_i = b_i.replace(' ', '')
            if name in b_i:
                result.append(b)
                break
    return result


def main():
    app.run(host='0.0.0.0', debug=True)

    # Test code
    # while True:
    #     name = input()
    #     book = find_book_by_name(name)
    #     print(book)


if __name__ == '__main__':
    main()
