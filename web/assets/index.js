function sendData(button) {
    // Retrieving the URL from the button's data attribute
    let data = button.getAttribute('data-url');

    // Making a fetch request to your Flask server
    fetch('/receive_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}