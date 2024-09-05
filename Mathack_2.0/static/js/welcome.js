document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('chatForm');
    const typingIndicator = document.querySelector('.typing');

    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent default form submission
        const message = document.getElementById('message').value;

        if (message.trim() !== "") {
            // Show typing indicator
            typingIndicator.style.display = 'flex';

            // Simulate message processing delay
            setTimeout(() => {
                // Hide typing indicator after a delay
                typingIndicator.style.display = 'none';

                // Submit the form after the delay (to simulate the bot's response)
                form.submit();
            }, 2000); // You can adjust the delay as needed
        }
    });
});
