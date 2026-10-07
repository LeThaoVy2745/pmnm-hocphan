from flask import Flask, jsonify, request, url_for, make_response
import csv
import io
from markupsafe import escape

app = Flask(__name__)

STUDENTS = {
    "23T1020001": {"name": "Nguyễn Văn An", "lop": "K47A", "scores": {"PMMNM": 8.5, "CSDL": 7.0, "MMT": 9.0}},
    "23T1020002": {"name": "Trần Thị Bình", "lop": "K47A", "scores": {"PMMNM": 6.0, "CSDL": 5.5, "MMT": 7.0}},
    "23T1020003": {"name": "Lê Hoàng Cường", "lop": "K47B", "scores": {"PMMNM": 9.5, "CSDL": 9.0}},
    "23T1020004": {"name": "Phạm Minh Dũng", "lop": "K47B", "scores": {"PMMNM": 4.0, "CSDL": 3.5, "MMT": 5.0}},
    "23T1020005": {"name": "Hoàng Thu Hà", "lop": "K47A", "scores": {}},
    "23T1020006": {"name": "Võ Quốc Khánh", "lop": "K47C", "scores": {"PMMNM": 7.5, "MMT": 8.0}},
}

def diem_tb(scores):
    if not scores:
        return None
    return sum(scores.values()) / len(scores)

def xep_loai(dtb):
    if dtb is None:
        return "-"
    if dtb >= 8.0:
        return "Giỏi"
    elif dtb >= 6.5:
        return "Khá"
    elif dtb >= 5.0:
        return "Trung bình"
    return "Yếu"

def render_layout(title, content):
    return f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            * {{ box-sizing: border-box; }}
            body {{ margin: 0; font-family: 'Segoe UI', Arial, sans-serif; background: #f4f7fb; color: #333; }}
            .container {{ width: 92%; max-width: 1000px; margin: 40px auto; }}
            
            .header {{ 
                background: linear-gradient(135deg, #2563eb, #1d4ed8); 
                color: white; 
                padding: 30px; 
                border-radius: 16px; 
                margin-bottom: 25px; 
                box-shadow: 0 4px 20px rgba(37, 99, 235, 0.2);
            }}
            .header h1 {{ margin: 0 0 15px; font-size: 26px; font-weight: 700; letter-spacing: 0.5px; }}
            
            .nav {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }}
            .nav a {{ 
                color: white; 
                text-decoration: none; 
                font-weight: 600; 
                font-size: 14px;
                background: rgba(255, 255, 255, 0.15); 
                padding: 8px 16px; 
                border-radius: 8px; 
                transition: all 0.2s ease;
                display: inline-block;
                white-space: nowrap;
            }}
            .nav a:hover {{ background: white; color: #2563eb; transform: translateY(-1px); }}
            
            .card {{ 
                background: white; 
                padding: 25px; 
                border-radius: 16px; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.05); 
                margin-bottom: 20px; 
            }}
            .card h2, .card h3 {{ margin-top: 0; color: #1e293b; }}
            
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
            th {{ background: #f8fafc; color: #475569; padding: 14px; text-align: left; font-size: 14px; border-bottom: 2px solid #e2e8f0; }}
            td {{ padding: 14px; border-bottom: 1px solid #f1f5f9; font-size: 15px; }}
            tr:hover {{ background: #f8fafc; }}
            
            .btn {{ 
                display: inline-block; 
                background: #2563eb; 
                color: white; 
                padding: 10px 18px; 
                text-decoration: none; 
                border-radius: 8px; 
                font-weight: 600; 
                border: none; 
                cursor: pointer; 
                font-size: 14px;
                transition: all 0.2s;
            }}
            .btn:hover {{ background: #1d4ed8; }}
            .input-text {{ width: 100%; max-width: 400px; padding: 11px 15px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 15px; outline: none; }}
            .input-text:focus {{ border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>HỆ THỐNG QUẢN LÝ SINH VIÊN</h1>
                <div class="nav">
                    <a href="{url_for('home')}">Trang chủ</a>
                    <a href="{url_for('student_list')}">Danh sách SV</a>
                    <a href="{url_for('search')}">Tìm kiếm</a>
                    <a href="/sv/23T1020001">Test Direct 301</a>
                </div>
            </div>
            {content}
        </div>
    </body>
    </html>
    """

@app.route("/")
def home():
    tong_sv = len(STUDENTS)
    ds_lop = sorted(set(sv["lop"] for sv in STUDENTS.values()))
    
    content = f"""
    <div style="display: flex; gap: 20px; margin-bottom: 20px; flex-wrap: wrap;">
        <div class="card" style="flex: 1; min-width: 200px; text-align: center;">
            <h2 style="color: #2563eb; font-size: 42px; margin: 0 0 5px; font-weight: 700;">{tong_sv}</h2>
            <p style="margin: 0; color: #64748b; font-size: 15px;">Tổng số sinh viên</p>
        </div>
        <div class="card" style="flex: 1; min-width: 200px; text-align: center;">
            <h2 style="color: #2563eb; font-size: 42px; margin: 0 0 5px; font-weight: 700;">{len(ds_lop)}</h2>
            <p style="margin: 0; color: #64748b; font-size: 15px;">Tổng số lớp học</p>
        </div>
    </div>
    <div class="card">
        <h3>Chức năng nhanh</h3>
        <p><a class="btn" href="{url_for('student_list')}">Xem Danh Sách Sinh Viên</a></p>
    </div>
    """
    return render_layout("Trang Chủ - Quản Lý Sinh Viên", content)

@app.route("/students")
def student_list():
    lop_filter = request.args.get("lop")
    ds_lop = sorted(set(sv["lop"] for sv in STUDENTS.values()))
    
    bg_all = "#2563eb" if not lop_filter else "#e2e8f0"
    color_all = "white" if not lop_filter else "#475569"
    filter_html = f'<a class="btn" style="background:{bg_all}; color:{color_all}; margin-right:8px; margin-bottom:8px;" href="{url_for("student_list")}">Tất cả</a>'
    
    for l in ds_lop:
        bg = "#2563eb" if lop_filter == l else "#e2e8f0"
        color = "white" if lop_filter == l else "#475569"
        filter_html += f'<a class="btn" style="background:{bg}; color:{color}; margin-right:8px; margin-bottom:8px;" href="{url_for("student_list", lop=l)}">{l}</a>'
        
    table_rows = ""
    for mssv, sv in STUDENTS.items():
        if lop_filter and sv["lop"].lower() != lop_filter.lower():
            continue
            
        dtb = diem_tb(sv["scores"])
        dtb_str = f"{dtb:.2f}" if dtb is not None else "-"
        xl = xep_loai(dtb)
        
        detail_link = url_for("student_detail", mssv=mssv)
        table_rows += f"""
        <tr>
            <td><a href="{detail_link}" style="color:#2563eb; font-weight:600; text-decoration:none;">{mssv}</a></td>
            <td>{escape(sv["name"])}</td>
            <td><span style="background:#dbeafe; color:#1d4ed8; padding:4px 10px; border-radius:12px; font-size:13px; font-weight:600;">{sv["lop"]}</span></td>
            <td>{dtb_str}</td>
            <td><b>{xl}</b></td>
        </tr>
        """
        
    if not table_rows:
        table_rows = '<tr><td colspan="5" style="text-align:center; color:#64748b;">Không tìm thấy sinh viên nào phù hợp.</td></tr>'

    content = f"""
    <div class="card">
        <h3 style="margin-bottom: 12px;">Lọc theo lớp:</h3>
        <div style="display:flex; flex-wrap:wrap;">{filter_html}</div>
    </div>
    <div class="card">
        <h2>Danh sách sinh viên</h2>
        <table>
            <tr>
                <th>MSSV</th>
                <th>Họ và tên</th>
                <th>Lớp</th>
                <th>Điểm TB</th>
                <th>Xếp loại</th>
            </tr>
            {table_rows}
        </table>
    </div>
    """
    return render_layout("Danh Sách Sinh Viên", content)

@app.route("/students/<mssv>")
def student_detail(mssv):
    if mssv not in STUDENTS:
        return render_404(None)

    sv = STUDENTS[mssv]
    dtb = diem_tb(sv["scores"])
    dtb_str = f"{dtb:.2f}" if dtb is not None else "-"
    
    score_rows = ""
    for mon, diem in sv["scores"].items():
        score_rows += f"<tr><td>{escape(mon)}</td><td><b>{diem}</b></td></tr>"
    if not score_rows:
        score_rows = '<tr><td colspan="2" style="color:#64748b;">Chưa có điểm học phần nào.</td></tr>'

    content = f"""
    <div class="card">
        <h2>Thông Tin Sinh Viên: {escape(sv["name"])}</h2>
        <p style="margin: 8px 0;"><b>MSSV:</b> {escape(mssv)}</p>
        <p style="margin: 8px 0;"><b>Lớp:</b> {escape(sv["lop"])}</p>
        <p style="margin: 8px 0;"><b>Điểm TB:</b> {dtb_str} | <b>Xếp loại:</b> {xep_loai(dtb)}</p>
        
        <h3 style="margin-top:20px;">Bảng điểm chi tiết</h3>
        <table>
            <tr><th>Môn học</th><th>Điểm</th></tr>
            {score_rows}
        </table>
        <br>
        <div style="display:flex; gap:10px;">
            <a class="btn" href="{url_for('export_csv', mssv=mssv)}">Xuất Bảng Điểm CSV</a>
            <a class="btn" style="background:#64748b;" href="{url_for('student_list')}">Quay lại danh sách</a>
        </div>
    </div>
    """
    return render_layout(f"Chi tiết - {mssv}", content)

@app.errorhandler(404)
def render_404(e):
    content = """
    <div class="card" style="text-align:center; padding:50px 20px;">
        <h1 style="font-size:72px; color:#ef4444; margin:0;">404</h1>
        <h2>Trang không tồn tại</h2>
        <p style="color:#64748b;">Dữ liệu hoặc đường dẫn bạn đang truy cập không tồn tại trên hệ thống.</p>
        <a class="btn" href="/">Về trang chủ</a>
    </div>
    """
    return render_layout("404 - Not Found", content), 404

@app.route("/sv/<mssv>")
def short_student(mssv):
    if mssv not in STUDENTS:
        return render_404(None)
    return "", 301, {"Location": url_for("student_detail", mssv=mssv)}

@app.route("/students/<mssv>/export")
def export_csv(mssv):
    if mssv not in STUDENTS:
        return render_404(None)

    sv = STUDENTS[mssv]
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(["MSSV", "Ho Ten", "Lop", "Mon Hoc", "Diem"])
    if sv["scores"]:
        for mon, diem in sv["scores"].items():
            writer.writerow([mssv, sv["name"], sv["lop"], mon, diem])
    else:
        writer.writerow([mssv, sv["name"], sv["lop"], "Chua co diem", "N/A"])

    response = make_response(output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = f"attachment; filename=diem_{mssv}.csv"
    return response

@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    results = []
    
    if q:
        q_lower = q.lower()
        for mssv, sv in STUDENTS.items():
            if q_lower in mssv.lower() or q_lower in sv["name"].lower():
                results.append((mssv, sv))

    result_rows = ""
    for mssv, sv in results:
        result_rows += f"""
        <tr>
            <td><a href="{url_for('student_detail', mssv=mssv)}" style="color:#2563eb; font-weight:600; text-decoration:none;">{mssv}</a></td>
            <td>{escape(sv["name"])}</td>
            <td><span style="background:#dbeafe; color:#1d4ed8; padding:4px 10px; border-radius:12px; font-size:13px; font-weight:600;">{sv["lop"]}</span></td>
        </tr>
        """
        
    content = f"""
    <div class="card">
        <h2 style="margin-bottom:15px;">Tìm kiếm sinh viên</h2>
        <form action="{url_for('search')}" method="GET" style="display:flex; gap:10px; flex-wrap:wrap;">
            <input type="text" name="q" value="{escape(q)}" class="input-text" placeholder="Nhập tên hoặc MSSV cần tìm...">
            <button type="submit" class="btn">Tìm kiếm</button>
        </form>
    </div>
    <div class="card">
        <h3>Kết quả tìm kiếm cho: "{escape(q)}"</h3>
        {"<table><tr><th>MSSV</th><th>Họ tên</th><th>Lớp</th></tr>" + result_rows + "</table>" if result_rows else "<p style='color:#64748b;'>Không tìm thấy dữ liệu phù hợp.</p>"}
    </div>
    """
    return render_layout("Tìm kiếm sinh viên", content)

@app.route("/api/students", methods=["GET"])
def api_students():
    return jsonify({
        "status": "success",
        "data": STUDENTS
    }), 200

@app.route("/api/score", methods=["POST"])
def api_update_score():
    data = request.get_json() or {}
    mssv = data.get("mssv")
    mon = data.get("mon")
    diem = data.get("diem")

    if not mssv or not mon or diem is None:
        return jsonify({"status": "error", "message": "Thiếu dữ liệu (mssv, mon, diem)"}), 400

    if mssv not in STUDENTS:
        return jsonify({"status": "error", "message": "Không tìm thấy sinh viên"}), 404

    try:
        diem_val = float(diem)
        STUDENTS[mssv]["scores"][mon] = diem_val
        dtb = diem_tb(STUDENTS[mssv]["scores"])
        
        return jsonify({
            "status": "success",
            "message": f"Đã cập nhật điểm môn {mon} cho SV {mssv}",
            "student": STUDENTS[mssv],
            "diem_trung_binh": round(dtb, 2)
        }), 200
    except ValueError:
        return jsonify({"status": "error", "message": "Điểm số phải là dạng số"}), 400

@app.errorhandler(Exception)
def handle_global_error(e):
    if request.path.startswith("/api/"):
        return jsonify({
            "status": "error",
            "message": "Đã xảy ra lỗi nội bộ trên server!"
        }), 500
        
    content = """
    <div class="card" style="text-align:center; padding:50px 20px;">
        <h1 style="color:#dc2626; margin:0;">500</h1>
        <h2>Lỗi Hệ Thống</h2>
        <p style="color:#64748b;">Hệ thống vừa gặp phải một sự cố ngoài ý muốn. Vui lòng thử lại sau!</p>
        <a class="btn" href="/">Quay lại trang chủ</a>
    </div>
    """
    return render_layout("500 - System Error", content), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)