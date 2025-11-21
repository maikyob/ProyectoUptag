// AJAX para cargar productos según servicio
document.getElementById('servicio-select').addEventListener('change', function() {
	const servicioId = this.value;
	const servicioPrecio = parseFloat(this.options[this.selectedIndex].getAttribute('data-precio'));
	const productoSelect = document.getElementById('producto-select');
	productoSelect.innerHTML = '<option value="">Selecciona un producto</option>';
	productoSelect.setAttribute('data-servicio-precio', isNaN(servicioPrecio) ? 0 : servicioPrecio);
	if (servicioId) {
		fetch(`/productos_por_servicio/?servicio_id=${servicioId}`)
			.then(response => response.json())
			.then(data => {
				data.productos.forEach(prod => {
					const option = document.createElement('option');
					option.value = prod.id;
					option.textContent = prod.nombre + ' ($' + prod.precio.toFixed(2) + ')';
					option.setAttribute('data-precio', prod.precio);
					productoSelect.appendChild(option);
				});
			});
	}
});

// Agregar producto a la lista de compra
const productoSelect = document.getElementById('producto-select');
const listaCompra = document.getElementById('lista-compra');
const totalPagar = document.getElementById('total-pagar');
let productosCompra = [];

productoSelect.addEventListener('change', function() {
	const selectedOption = this.options[this.selectedIndex];
	const prodId = selectedOption.value;
	const prodNombre = selectedOption.textContent;
	const prodPrecio = parseFloat(selectedOption.getAttribute('data-precio'));
	const servicioPrecio = parseFloat(this.getAttribute('data-servicio-precio'));
	let precioFinal = servicioPrecio > 0 ? servicioPrecio : prodPrecio;
	if (prodId && !productosCompra.some(p => p.id === prodId)) {
		productosCompra.push({id: prodId, nombre: prodNombre, precio: precioFinal});
		actualizarListaCompra();
	}
});

function actualizarListaCompra() {
	listaCompra.innerHTML = '';
	let total = 0;
	productosCompra.forEach(prod => {
		total += prod.precio;
		const li = document.createElement('li');
		li.textContent = prod.nombre + ' - $' + prod.precio.toFixed(2);
		// Botón para eliminar producto
		const btnDel = document.createElement('button');
		btnDel.textContent = 'Eliminar';
		btnDel.className = 'btn btn-sm btn-danger ms-2';
		btnDel.onclick = function() {
			productosCompra = productosCompra.filter(p => p.id !== prod.id);
			actualizarListaCompra();
		};
		li.appendChild(btnDel);
		listaCompra.appendChild(li);
	});
	totalPagar.textContent = total.toFixed(2);
}