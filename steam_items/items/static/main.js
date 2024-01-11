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
    }).catch(function(error) {
        console.error('Ошибка при обновлении цены: ', error);
        var arrowField = document.getElementById('arrow_' + itemId);
        arrowField.className = 'item-label error';
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

/**
 * Обновляет цену предмета без перезагрузки страницы.
 * 
 * @param {string} itemId - ID предмета, цену которого нужно обновить.
 * @param {number} attempt - Номер текущей попытки обновления цены (по умолчанию 1).
 * @returns {Promise} Promise, который разрешается с объектом, содержащим два свойства:
 *                    `success`, который равен `true`, если обновление прошло успешно, и `false` в противном случае,
 *                    и `priceChanged`, который равен `true`, если цена изменилась, и `false` в противном случае.
 */
function updatePriceWithoutReload(itemId, attempt = 1) {
    var oldPrice = parseFloat(document.getElementById('current_price_' + itemId).value);

    return new Promise(function(resolve, reject) {
        setTimeout(function() {
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
                    var contentType = response.headers.get("content-type");
                    if (contentType && contentType.includes("application/json")) {
                        return response.json();
                    } else {
                        throw new Error('Ошибка: ответ не содержит JSON');
                    }
                } else {
                    throw new Error('Ошибка сети.');
                }
            }).then(function(data) {
                var currentPrice = data.new_price;
                var arrowField = document.getElementById('arrow_' + itemId);
                arrowField.className = 'item-label';
                if (oldPrice !== undefined && data.price_direction === 'up') {
                    arrowField.classList.add('arrow-up');
                    resolve({success: true, priceChanged: true});
                } else if (oldPrice !== undefined && data.price_direction === 'down') {
                    arrowField.classList.add('arrow-down');
                    resolve({success: true, priceChanged: true});
                } else if (oldPrice === currentPrice) {
                    arrowField.classList.add('arrow-none');
                    resolve({success: true, priceChanged: false});
                }

                document.getElementById('current_price_' + itemId).value = currentPrice;
            }).catch(function(error) {
                console.error('Ошибка при обновлении цены: ', error);
                var arrowField = document.getElementById('arrow_' + itemId);
                arrowField.className = 'item-label error';
                if (attempt < 5) {
                    resolve(updatePriceWithoutReload(itemId, attempt + 1));
                } else {
                    resolve({success: false});
                }
            });
        }, 2000);
    });
}

/**
 * Обновляет цены всех предметов на странице.
 * 
 * Функция проходит по всем ID предметов в глобальном массиве `itemIds` и вызывает `updatePriceWithoutReload` для каждого из них.
 * После обновления всех цен функция отображает сообщение с количеством обновлений.
 */
function updateAllPrices() {
    var successfulUpdates = 0;
    var failedUpdates = 0;
    var unchangedPrices = 0;

    function updateNextItem(i) {
        if (i < itemIds.length) {
            updatePriceWithoutReload(itemIds[i])
                .then(function(result) {
                    if (result.success) {
                        successfulUpdates++;
                        if (!result.priceChanged) {
                            unchangedPrices++;
                        }
                    } else {
                        failedUpdates++;
                    }
                    updateNextItem(i + 1);
                });
        } else {
            alert('Успешно обновлено ' + successfulUpdates + ' цен. Не удалось обновить ' + failedUpdates + ' цен. Цены ' + unchangedPrices + ' предметов не изменились. Пожалуйста, перезагрузите страницу.');
        }
    }
    updateNextItem(0);
}
