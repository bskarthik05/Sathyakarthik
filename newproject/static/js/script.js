document.getElementById('loginForm').addEventListener('submit', function(event) {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!username || !password) {
        event.preventDefault();
        alert("Please fill in both username and password.");
    } else {
        alert("Login form submitted! Replace this with backend validation.");
    }
});