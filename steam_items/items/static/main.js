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

function saveCurrentPrice(itemId) {
    var currentPrice = document.getElementById('current_price_' + itemId).value;
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
            location.reload();
        } else {
            throw new Error('Ошибка сети.');
        }
    });
}




function handleKeyPress(event, itemId) {
    if (event.key === 'Enter') {
        event.preventDefault();
        document.getElementById('current_price_' + itemId).blur();
    }
}
