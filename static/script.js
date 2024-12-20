// script.js

document.addEventListener('DOMContentLoaded', function() {
    // Función para validar el formulario de agregar producto
    function validarFormularioAgregar() {
        var nombre = document.getElementById('nombre').value.trim();
        var precio = document.getElementById('precio').value.trim();

        if (nombre === '' || precio === '') {
            alert('Por favor, complete todos los campos.');
            return false;
        }

        if (isNaN(precio) || parseFloat(precio) <= 0) {
            alert('El precio debe ser un número válido mayor a cero.');
            return false;
        }

        return true;
    }

    // Asigna la función de validación al evento de envío del formulario
    var formAgregar = document.getElementById('form-agregar');
    if (formAgregar) {
        formAgregar.addEventListener('submit', function(event) {
            if (!validarFormularioAgregar()) {
                event.preventDefault();
            }
        });
    }

    // Confirmación eliminar producto
    var botonesEliminar = document.querySelectorAll('.btn-eliminar');
    botonesEliminar.forEach(function(boton) {
        boton.addEventListener('click', function(event) {
            var confirmar = confirm('¿Estás seguro de que deseas eliminar este producto?');
            if (!confirmar) {
                event.preventDefault();  // Previene que se envíe el enlace si la confirmación falla
            }
        });
    });
});