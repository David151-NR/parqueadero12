$(document).ready(function() {
    // Función para calcular el precio
    function calculatePrice(entryTime, exitTime) {
        const priceTable = [
            { hours: 1, price: 2000 },
            { hours: 2, price: 3500 },
            { hours: 4, price: 5000 },
            { hours: 8, price: 8000 },
            { hours: 12, price: 10000 },
            { hours: 24, price: 15000 }
        ];
    
        let diff = (exitTime - entryTime) / (1000 * 3600); // Diferencia en horas
        let totalPrice = 0;
    
        if (diff <= 24) {
            // Buscar el precio adecuado para menos de 24 horas
            for (let i = 0; i < priceTable.length; i++) {
                if (diff <= priceTable[i].hours) {
                    totalPrice = priceTable[i].price;
                    break;
                }
            }
        } else {
            // Calcular cuántos días completos hay
            let fullDays = Math.floor(diff / 24);
            let remainingHours = diff % 24;
    
            totalPrice = fullDays * 15000;
    
            // Calcular precio adicional por las horas restantes
            for (let i = 0; i < priceTable.length; i++) {
                if (remainingHours <= priceTable[i].hours) {
                    totalPrice += priceTable[i].price;
                    break;
                }
            }
        }
    
        return totalPrice;
    }

    // Evento para cuando se envía el formulario
    $('#parkingForm').submit(function(event) {
        event.preventDefault();
        let entryTime = new Date($('#entryTime').val());
        let exitTime = new Date($('#exitTime').val());       
        if (entryTime > exitTime) {
            alert("La hora de salida debe ser posterior a la hora de entrada.");
            return;
        }

        let totalPrice = calculatePrice(entryTime, exitTime);
        $('#totalPrice').text('$' + totalPrice.toLocaleString());
    });
});
