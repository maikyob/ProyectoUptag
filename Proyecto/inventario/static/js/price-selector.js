;(function($){
    $(function(){
        // When a product select changes, fill the corresponding price input.
        // Usage HTML (per row):
        // <select class="product-select" name="producto">
        //   <option value="{{ p.id }}" data-price="{{ p.precio_venta }}">{{ p.nombre }}</option>
        // </select>
        // <input type="text" class="price-input" name="precio">

        $(document).on('change', '.product-select', function(){
            var $sel = $(this);
            var $row = $sel.closest('tr, .row, .item-row');
            var price = $sel.find('option:selected').data('price');
            var $priceInput = $row.find('.price-input');
            if (price === undefined){
                // If no data-price found, try to fetch from server (optional endpoint)
                var id = $sel.val();
                if (!id){ return; }
                // Try AJAX GET to /product-price/?id=ID which you can implement server-side
                $.getJSON('/product-price/', { id: id })
                    .done(function(resp){
                        if (resp && resp.price !== undefined){
                            $priceInput.val(resp.price);
                        }
                    })
                    .fail(function(){
                        // nothing
                    });
                return;
            }
            // set value with two decimals
            if ($priceInput.length){
                $priceInput.val(parseFloat(price).toFixed(2));
            }
        });

        // Optional: when adding new rows dynamically, you may want to trigger change
        // Example: after appending row -> $(row).find('.product-select').trigger('change');

        // Convenience: auto-update total per row when price or qty changes
        $(document).on('input change', '.price-input, .qty-input', function(){
            var $row = $(this).closest('tr, .row, .item-row');
            var qty = parseFloat(($row.find('.qty-input').val()||0));
            var price = parseFloat(($row.find('.price-input').val()||0));
            var $total = $row.find('.row-total');
            if ($total.length){
                $total.text( (qty * price).toFixed(2) );
            }
            // Optionally update summary total
            updateSummaryTotal();
        });

        function updateSummaryTotal(){
            var sum = 0;
            $('.row-total').each(function(){
                var v = parseFloat($(this).text() || 0);
                if (!isNaN(v)) sum += v;
            });
            var $summary = $('.summary-total');
            if ($summary.length){
                $summary.text(sum.toFixed(2));
            }
        }

    });
})(jQuery);
