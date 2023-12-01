// Wait for the DOM content to be fully loaded before executing the script
document.addEventListener('DOMContentLoaded', function() {
    // Get all elements with the class 'result-title'
    var resultLinks = document.getElementsByClassName('post-link');

    // Add a click event listener to each result title link
    for (var i = 0; i < resultLinks.length; i++) {
        resultLinks[i].addEventListener('click', function(event) {
            // Prevent the default link behavior (opening in the same tab)
            event.preventDefault();

            // Get the URL from the 'href' attribute of the clicked link
            var url = this.getAttribute('href');
            
            // Open the URL in a new tab
            window.open(url, '_blank');

            // Send an API request to the '/addView' endpoint inside the frontend
            fetch('/addView', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 'site': url }),
            })
            .then(response => {
                // Handle the response as needed
                if (!response.ok) {
                    console.error('Error:', response.status, response.statusText);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});
