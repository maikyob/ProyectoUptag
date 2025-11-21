;(function($){
    $(function(){
        var $form = $('form');
        if ($form.length === 0) return;

        var $alerts = $('.service-alerts');
        if ($alerts.length === 0){
            $alerts = $('<div class="service-alerts mb-3"></div>');
            $form.before($alerts);
        }

        function showAlert(msg, type){
            var cls = 'alert-' + (type || 'danger');
            var $a = $('<div class="alert ' + cls + '" role="alert"></div>').text(msg);
            $alerts.empty().append($a);
        }

        $form.on('submit', function(e){
            e.preventDefault();
            var action = $form.attr('action') || window.location.href;
            var data = $form.serialize();
            var $submit = $form.find('button[type="submit"]');
            $submit.prop('disabled', true);

            $.ajax({
                url: action,
                method: 'POST',
                data: data,
                dataType: 'json',
                success: function(resp){
                    if (resp && resp.success){
                        // si devuelve redirect, seguirlo
                        if (resp.redirect){ window.location.href = resp.redirect; return; }
                        showAlert('Servicio guardado correctamente.', 'success');
                        $submit.prop('disabled', false);
                    } else {
                        showAlert('No se pudo guardar el servicio. Intente nuevamente.');
                        $submit.prop('disabled', false);
                    }
                },
                error: function(xhr){
                    if (xhr && xhr.status === 400 && xhr.responseJSON && xhr.responseJSON.errors){
                        var msgs = [];
                        var errors = xhr.responseJSON.errors;
                        for (var f in errors){
                            if (!errors.hasOwnProperty(f)) continue;
                            msgs = msgs.concat(errors[f]);
                        }
                        showAlert(msgs.join('; '));
                    } else if (xhr && xhr.status === 200 && xhr.responseText && xhr.responseText.indexOf('<!DOCTYPE') === 0){
                        // fallback a submit normal
                        $form.off('submit');
                        $form.submit();
                        return;
                    } else {
                        showAlert('Ocurrió un error al guardar. Intente nuevamente.');
                    }
                    $submit.prop('disabled', false);
                }
            });
        });
    });
})(jQuery);
