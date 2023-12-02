function setDataFromInput() {
    let userInput = document.getElementById('inputboxfield').value;
    let button = document.getElementById('inputButton');
    button.setAttribute('data-url', userInput);
}

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

function toggleCategory(button) {
    let content = button.parentNode.nextElementSibling;
    if (content.style.display === "block") {
        content.style.display = "none";
        if (button.classList.contains('category-button-open')) {
            button.classList.remove('category-button-open');
            button.classList.add('category-button');
        }
    } else {
        content.style.display = "block";
        if (button.classList.contains('category-button')) {
            button.classList.remove('category-button');
            button.classList.add('category-button-open');
        }
    }
}