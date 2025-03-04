from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Настройка подключения к базе SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pois.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель для точки интереса
class POI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)

# Главная страница: отображает карту с точками
@app.route('/')
def index():
    pois = POI.query.all()
    return render_template('index.html', pois=pois)

# Эндпоинт для добавления новой точки через AJAX
@app.route('/add_poi', methods=['POST'])
def add_poi():
    data = request.get_json()
    name = data.get('name', 'Без названия')
    description = data.get('description', '')
    lat = data.get('lat')
    lng = data.get('lng')
    if lat is None or lng is None:
        return jsonify({'error': 'Нет координат'}), 400
    new_poi = POI(name=name, description=description, lat=lat, lng=lng)
    db.session.add(new_poi)
    db.session.commit()
    return jsonify({'success': True, 'id': new_poi.id})

if __name__ == '__main__':
    # Создаёт базу и таблицы, если их ещё нет
    db.create_all()
    app.run(debug=True)
