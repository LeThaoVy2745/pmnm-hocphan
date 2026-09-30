# from flask import Flask, request
# from werkzeug import routing
# app = Flask(__name__)
# @app.route("/")
# def index():
#     about_link = url_for('gioi_thieu')
#     return f"<a href='/'>Trang chu</a> | <a href='{about_link}'>Trang gioi thieu</a>"
# @app.route("/sum/<strs>")
# def tong(strs):
#     #1,2,3=6
#     numbers = strs.split(",")
#     total = sum(float(num) for num in numbers)
#     return f"tong cuar {strs} la: {total}"



# @app.route("/tinh-toan")
# def tinh_toan():
#     a = request.args.get("a", float)
#     b = request.args.get("b", float)
#     op=request.args.get("op")
#     if a is None:
#         return f"Vui long nhap a"
#     if op=="add":
#         return f"{a} + {b} ={float(a) + float(b)}"
#     elif op=="sub":
#         return f"{a} - {b} = {float(a) - float(b)} "
#     return f"Gia tri cua a va b: {a} {b}"

# @app.route("/gioi-thieu")
# @app.route("/about")

# @app.route("/square/<float:x>")
# def square(x):
#     return f"Gtri bp {x} la {x**2}"
# def gioi_thieu():
#     return "xin chao, day la trang gioi thieu!"
# if __name__ =="__main__":
#     app.run(debug=False)

from flask import Flask, request, jsonify, abort, url_for
from markupsafe import escape

app = Flask(__name__)

BOOKS = [
    {"id": 1, "title": "Lap trinh Python", "author": "Nguyen Van A", "year": 2023, "category": "Lap trinh", "available": True},
    {"id": 2, "title": "Flask Web co ban", "author": "Tran Van B", "year": 2022, "category": "Lap trinh", "available": True},
    {"id": 3, "title": "Co so du lieu SQL", "author": "Le Thi C", "year": 2021, "category": "Co so du lieu", "available": False},
    {"id": 4, "title": "Mang may tinh", "author": "Pham Van D", "year": 2024, "category": "Mang", "available": True}
]

CSS_STYLE = '''
<style>
    body { font-family: Arial, sans-serif; background: #ffffff; margin: 0; padding: 20px; color: #333; }
    .container { max-width: 800px; margin: 0 auto; padding: 10px; }
    nav { background: #f8f9fa; padding: 10px; border: 1px solid #ddd; border-radius: 4px; margin-bottom: 20px; }
    nav a { color: #007bff; text-decoration: none; font-weight: bold; margin-right: 15px; }
    nav a:hover { text-decoration: underline; }
    h2 { color: #222; border-bottom: 1px solid #ccc; padding-bottom: 5px; }
    .btn-filter { display: inline-block; padding: 4px 8px; background: #f1f1f1; color: #333; text-decoration: none; border-radius: 3px; font-size: 13px; margin-right: 5px; border: 1px solid #ccc; }
    .btn-filter:hover { background: #e2e2e2; }
    table { width: 100%; border-collapse: collapse; margin-top: 15px; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background: #f2f2f2; }
    .status-yes { color: green; font-weight: bold; }
    .status-no { color: red; font-weight: bold; }
    .card { background: #fafafa; border: 1px solid #e0e0e0; padding: 15px; margin: 15px 0; border-radius: 4px; }
    a.book-link { color: #007bff; text-decoration: none; font-weight: bold; }
    a.book-link:hover { text-decoration: underline; }
</style>
'''

def get_header(title):
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        {CSS_STYLE}
    </head>
    <body>
        <div class="container">
            <nav>
                <a href="{url_for('index')}">Trang chu</a>
                <a href="{url_for('get_books')}">Danh sach sach</a>
                <a href="{url_for('api_get_books')}">API Books</a>
            </nav>
    '''

def get_footer():
    return '''
        </div>
    </body>
    </html>
    '''

@app.route("/")
def index():
    tong_so_sach = len(BOOKS)
    sach_san_sang = sum(1 for b in BOOKS if b["available"])

    return get_header("Trang chu") + f'''
        <h2>Thong ke thu vien</h2>
        <div class="card">
            <p>Tong so dau sach: <b>{tong_so_sach}</b></p>
            <p>So sach san sang cho muon: <b>{sach_san_sang}</b></p>
        </div>
    ''' + get_footer()

@app.route("/books")
def get_books():
    category = request.args.get("category")

    rows = ""
    for book in BOOKS:
        if category and book["category"].lower() != category.lower():
            continue

        trang_thai = '<span class="status-yes">Co san</span>' if book["available"] else '<span class="status-no">Da muon</span>'
        link_chi_tiet = url_for('get_book_detail', book_id=book['id'])
        
        rows += f'''
        <tr>
            <td>{book['id']}</td>
            <td><a class="book-link" href="{link_chi_tiet}">{escape(book['title'])}</a></td>
            <td>{escape(book['author'])}</td>
            <td>{escape(book['category'])}</td>
            <td>{trang_thai}</td>
        </tr>
        '''

    return get_header("Danh sach sach") + f'''
        <h2>Danh sach sach</h2>
        <div style="margin-bottom: 15px;">
            <b>The loai:</b> 
            <a class="btn-filter" href="{url_for('get_books')}">Tat ca</a>
            <a class="btn-filter" href="{url_for('get_books', category='Lap trinh')}">Lap trinh</a>
            <a class="btn-filter" href="{url_for('get_books', category='Co so du lieu')}">Co so du lieu</a>
            <a class="btn-filter" href="{url_for('get_books', category='Mang')}">Mang</a>
        </div>
        <table>
            <tr>
                <th>ID</th>
                <th>Ten sach</th>
                <th>Tac gia</th>
                <th>The loai</th>
                <th>Trang thai</th>
            </tr>
            {rows}
        </table>
    ''' + get_footer()

@app.route("/books/<int:book_id>")
def get_book_detail(book_id):
    sach_tim_thay = next((b for b in BOOKS if b["id"] == book_id), None)
    if sach_tim_thay is None:
        abort(404, description=f"Khong co sach voi ID = {book_id}")

    trang_thai = '<span class="status-yes">Co san</span>' if sach_tim_thay["available"] else '<span class="status-no">Da muon</span>'

    return get_header("Chi tiet sach") + f'''
        <h2>Chi tiet sach #{sach_tim_thay['id']}</h2>
        <div class="card">
            <p><b>Ten sach:</b> {escape(sach_tim_thay['title'])}</p>
            <p><b>Tac gia:</b> {escape(sach_tim_thay['author'])}</p>
            <p><b>Nam XB:</b> {sach_tim_thay['year']}</p>
            <p><b>The loai:</b> {escape(sach_tim_thay['category'])}</p>
            <p><b>Trang thai:</b> {trang_thai}</p>
        </div>
        <a href="{url_for('get_books')}" style="color: #007bff; text-decoration: none;">&larr; Quay lai danh sach</a>
    ''' + get_footer()

@app.route("/api/books")
def api_get_books():
    return jsonify(BOOKS)

@app.route("/api/books/<int:book_id>")
def api_get_book_detail(book_id):
    sach_tim_thay = next((b for b in BOOKS if b["id"] == book_id), None)
    if sach_tim_thay is None:
        return jsonify({"error": f"Khong tim thay sach voi ID = {book_id}"}), 404
    return jsonify(sach_tim_thay)

@app.errorhandler(404)
def page_not_found(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "404 Not Found"}), 404

    thong_bao = e.description if hasattr(e, 'description') else "Trang khong ton tai!"

    return get_header("Loi 404") + f'''
        <div style="padding: 20px 0;">
            <h3 style="color: red;">Loi 404: {escape(thong_bao)}</h3>
        </div>
    ''' + get_footer(), 404

if __name__ == "__main__":
    app.run(debug=True)