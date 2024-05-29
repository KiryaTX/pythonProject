from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reports.db'

db = SQLAlchemy(app)

# Создаем таблицу в базе данных
class Reportings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50))
    machine = db.Column(db.String(50))
    work = db.Column(db.String(50))

    def init(self, fullname, machine, work):
        self.fullname = fullname
        self.machine = machine
        self.work = work


with app.app_context():
    db.create_all()


# Метод для добавления репорта
@app.route('/add_report', methods=['POST'])
def add_report():
    fullname = request.form['fullname']
    machine = request.form['machine']
    work = request.form['work']
    report = Reportings(fullname, machine, work)
    db.session.add(report)
    db.session.commit()
    return {"success": 'Report added successfully'}


# Метод для получения отчетов по id сотрудника
@app.route('/get_report_for_id/<int:id>')
def get_report_for_id(id):
    report = Reportings.query.get(id)
    if report:
        return jsonify({
            'fullname': report.fullname,
            'machine': report.machine,
            'work': report.work
        })
    else:
        return {'error': 'Report_for_id not found'}

# Метод для получения списка всех отчетов
@app.route('/get_all_reports', methods=['GET'])
def get_all_reports():
    report = Reportings.query.all()
    response = []
    for report in report:
        response.append({
            'id': report.id,
            'fullname': report.fullname,
            'machine': report.machine,
            'work': report.work
        })
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)