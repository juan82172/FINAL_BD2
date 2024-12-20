from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/inventario_db"
app.secret_key = "supersecretkey"

mongo = PyMongo(app)

# Ruta principal
@app.route('/')
def index():
    prendas = mongo.db.prendas.find()
    return render_template('index.html', prendas=prendas)

# Agregar un producto
@app.route('/add', methods=['POST'])
def add_item():
    try:
        id_unico = request.form.get('id').zfill(4)
        nombre = request.form.get('nombre')
        categoria = request.form.get('categoría')
        precio = float(request.form.get('precio'))
        stock = int(request.form.get('stock'))

        # Validar ID de 4 caracteres
        if len(id_unico) != 4 or not id_unico.isdigit():
            flash("El ID debe ser un número de exactamente 4 dígitos.", "error")
            return redirect(url_for('index'))

        # Unicidad del ID
        if mongo.db.prendas.find_one({"id": id_unico}):
            flash("El ID ya existe. Por favor, ingresa un ID único.", "error")
            return redirect(url_for('index'))

        # Insertar en BD
        mongo.db.prendas.insert_one({
            "id": id_unico,
            "nombre": nombre,
            "categoría": categoria,
            "precio": precio,
            "stock": stock
        })

        flash("Producto agregado exitosamente.", "success")
        return redirect(url_for('index'))
    except ValueError:
        flash("Error en los datos ingresados. Verifica que sean correctos.", "error")
        return redirect(url_for('index'))

# Mostrar la lista de productos
@app.route('/reporte_prendas')
def reporte_prendas():
    prendas = mongo.db.prendas.find()
    return render_template('reporte_prendas.html', prendas=prendas)

# Eliminar un producto
@app.route('/delete/<id_unico>', methods=['POST'])
def delete_item(id_unico):
    mongo.db.prendas.delete_one({"id": id_unico})
    flash("Producto eliminado exitosamente.", "success")
    return redirect(url_for('reporte_prendas'))

# Editar un producto
@app.route('/edit/<id_unico>', methods=['GET', 'POST'])
def edit_item(id_unico):
    if request.method == 'GET':
        item = mongo.db.prendas.find_one({"id": id_unico})
        return render_template('editar.html', producto=item)
    else:
        try:
            nombre = request.form.get('nombre')
            categoria = request.form.get('categoría')
            precio = float(request.form.get('precio'))
            stock = int(request.form.get('stock'))

            mongo.db.prendas.update_one({"id": id_unico}, {
                "$set": {
                    "nombre": nombre,
                    "categoría": categoria,
                    "precio": precio,
                    "stock": stock
                }
            })
            flash("Producto actualizado exitosamente.", "success")
        except ValueError:
            flash("Error en los datos ingresados. Verifica que sean correctos.", "error")
        return redirect(url_for('reporte_prendas'))

if __name__ == '__main__':
    app.run(debug=True)