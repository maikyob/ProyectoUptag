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

// Permitir agregar desde el botón externo
window.agregarProductoVenta = function(producto) {
	if (producto.id && !productosCompra.some(p => p.id === producto.id)) {
		productosCompra.push(producto);
		actualizarListaCompra();
	}
}

// También permitir agregar desde el select (opcional)
productoSelect.addEventListener('change', function() {
	const selectedOption = this.options[this.selectedIndex];
	const prodId = selectedOption.value;
	const prodNombre = selectedOption.textContent;
	const prodPrecio = parseFloat(selectedOption.getAttribute('data-precio'));
	const servicioPrecio = parseFloat(this.getAttribute('data-servicio-precio'));
	let precioFinal = servicioPrecio > 0 ? servicioPrecio : prodPrecio;
	if (prodId && !productosCompra.some(p => p.id === prodId)) {
		window.agregarProductoVenta({id: prodId, nombre: prodNombre, precio: precioFinal});
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

if (typeof window.listaCompra === 'undefined') {
	window.listaCompra = [];
}
function actualizarTablaCompra() {
	const tbody = document.querySelector('#tabla-lista-compra tbody');
	tbody.innerHTML = '';
	let total = 0;
	window.listaCompra.forEach((item, idx) => {
		total += item.precio;
		const tr = document.createElement('tr');
		tr.innerHTML = `<td>${item.servicio}</td><td>${item.producto}</td><td>$${item.precio.toFixed(2)}</td><td><button type='button' class='btn btn-danger btn-sm' onclick='quitarItem(${idx})'>Quitar</button></td>`;
		tbody.appendChild(tr);
	});
	document.getElementById('total-pagar').textContent = total.toFixed(2);
}
function quitarItem(idx) {
	window.listaCompra.splice(idx, 1);
	actualizarTablaCompra();
}
document.getElementById('agregar-lista').addEventListener('click', function() {
	const servicioSelect = document.getElementById('servicio-select');
	const productoSelect = document.getElementById('producto-select');
	const servicioText = servicioSelect.options[servicioSelect.selectedIndex]?.text || '';
	const productoText = productoSelect.options[productoSelect.selectedIndex]?.text || '';
	let precioServicio = parseFloat(servicioSelect.options[servicioSelect.selectedIndex]?.getAttribute('data-precio')) || 0;
	let precioProducto = parseFloat(productoSelect.options[productoSelect.selectedIndex]?.getAttribute('data-precio')) || 0;
	let precio = precioServicio > 0 ? precioServicio : precioProducto;
	if(servicioSelect.value && productoSelect.value) {
		window.listaCompra.push({servicio: servicioText, producto: productoText, precio: precio});
		actualizarTablaCompra();
	} else {
		alert('Selecciona servicio y producto');
	}
});

// --- Autocompletar cliente por DNI ---
document.getElementById('dni').addEventListener('blur', function() {
	const dni = this.value.trim();
	if (dni.length > 0) {
		fetch(`/buscar_cliente/?dni=${dni}`)
			.then(response => response.json())
			.then(data => {
				if (data.encontrado) {
					document.getElementById('nombre').value = data.nombre;
					document.getElementById('email').value = data.email;
					document.getElementById('telefono').value = data.telefono;
					document.getElementById('direccion').value = data.direccion;
				} else {
					document.getElementById('nombre').value = '';
					document.getElementById('email').value = '';
					document.getElementById('telefono').value = '';
					document.getElementById('direccion').value = '';
					alert('Cliente no registrado. Por favor, ingresa los datos para agregarlo.');
				}
			})
			.catch(() => {
				alert('Error al buscar el cliente.');
			});
	}
});