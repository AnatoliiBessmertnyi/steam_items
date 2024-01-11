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

/**
 * Обновляет текущую цену предмета, делая POST-запрос к серверу, и обновляет стрелку, указывающую на изменение цены.
 * После обновления цены страница перезагружается через 2 секунды.
 *
 * @param {string} itemId - ID предмета, цену которого нужно обновить.
 *
 * При успешном обновлении цены этот метод обновляет стрелку, указывающую на изменение цены:
 * - Если цена увеличилась, добавляется класс 'arrow-up'.
 * - Если цена уменьшилась, добавляется класс 'arrow-down'.
 * - Если цена не изменилась, классы 'arrow-up' и 'arrow-down' не добавляются.
 *
 * Затем обновляет значение текущей цены в DOM.
 *
 * Наконец, устанавливает таймер для перезагрузки страницы через 2 секунды.
 *
 * @throws {Error} Если запрос к серверу не удался, выбрасывается ошибка с сообщением 'Ошибка сети.'.
 */
function updatePrice(itemId) {
    var oldPrice = parseFloat(document.getElementById('current_price_' + itemId).value);

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
            return response.json();
        } else {
            throw new Error('Ошибка сети.');
        }
    }).then(function(data) {
        var currentPrice = data.new_price;
        var arrowField = document.getElementById('arrow_' + itemId);
        arrowField.className = 'item-label';
        if (oldPrice !== undefined && data.price_direction === 'up') {
            arrowField.classList.add('arrow-up');
        } else if (oldPrice !== undefined && data.price_direction === 'down') {
            arrowField.classList.add('arrow-down');
        }

        document.getElementById('current_price_' + itemId).value = currentPrice;

        if (oldPrice !== currentPrice) {
            setTimeout(function() {
                location.reload();
            }, 2000);
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
