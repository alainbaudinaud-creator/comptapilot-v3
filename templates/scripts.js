// scripts.js
const sociétésTable = document.getElementById('sociétés-table').getElementsByTagName('tbody')[0];

fetch('/sociétés')
    .then(response => response.json())
    .then(data => {
        data.forEach(société => {
            const row = sociétésTable.insertRow();
            row.insertCell().textContent = société.id;
            row.insertCell().textContent = société.name;
            row.insertCell().textContent = société.address;
        });
    })
    .catch(error => console.error('Error:', error));

const addSociétéForm = document.getElementById('add-société-form');
addSociétéForm.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(addSociétéForm);
    fetch('/sociétés/add', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(Object.fromEntries(formData.entries()))
    })
    .then(response => response.json())
    .then(data => {
        const row = sociétésTable.insertRow();
        row.insertCell().textContent = data.id;
        row.insertCell().textContent = data.name;
        row.insertCell().textContent = data.address;
        addSociétéForm.reset();
    })
    .catch(error => console.error('Error:', error));
});