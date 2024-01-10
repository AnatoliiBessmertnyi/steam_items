/**
 * Получает значение куки по имени.
 *
 * @param {string} name - Имя куки.
 * @returns {string|null} Значение куки или null, если куки не найдено.
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Сохраняет текущую цену товара.
 *
 * @param {string} itemId - ID товара.
 */
function saveCurrentPrice(itemId) {
    var currentPrice = parseFloat(document.getElementById('current_price_' + itemId).value);
    var oldPrice = parseFloat(document.getElementById('old_current_price_' + itemId).value);

    fetch('/save_current_price/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            'item_id': itemId,
            'current_price': currentPrice
        })
    }).then(function(response) {
        if (response.ok) {
            var arrowField = document.getElementById('arrow_' + itemId);
            arrowField.className = 'item-label';
            if (oldPrice !== undefined && currentPrice > oldPrice) {
                arrowField.classList.add('arrow-up');
            } else if (oldPrice !== undefined && currentPrice < oldPrice) {
                arrowField.classList.add('arrow-down');
            }

            document.getElementById('old_current_price_' + itemId).value = currentPrice;

            setTimeout(function() {
                location.reload();
            }, 2000);
        } else {
            throw new Error('Ошибка сети.');
        }
    });
}

function updatePrice(itemId) {
    fetch('/update_price/' + itemId + '/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            'item_id': itemId
        })
    }).then(function(response) {
        if (response.ok) {
            setTimeout(function() {
                location.reload();
            }, 2000);
        } else {
            throw new Error('Ошибка сети.');
        }
    });
}

/**
 * Обрабатывает нажатие клавиши в поле ввода цены.
 *
 * @param {Event} event - Событие нажатия клавиши.
 * @param {string} itemId - ID товара.
 */
function handleKeyPress(event, itemId) {
    if (event.key === 'Enter') {
        event.preventDefault();
        document.getElementById('current_price_' + itemId).blur();
    }
}
