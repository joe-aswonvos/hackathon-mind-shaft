document.addEventListener("DOMContentLoaded", function()  {
    function confirmDeletion(deckId, cardId) {
        // Show confirmation dialog
        const userConfirmed = confirm("Are you sure you want to delete this card?");
        if (userConfirmed) {
            // Perform the DELETE operation using fetch
            fetch(`/deck/${deckId}/card/${cardId}/delete/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(), // Get CSRF token
                },
            })
            .then((response) => {
                if (response.ok) {
                    // Reload the page or remove the card element from the DOM
                    location.reload(); // This reloads the page
                } else {
                    alert("Failed to delete the card.");
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("An error occurred while deleting the card.");
            });
        }
    }

    function getCSRFToken() {
        // Fetch the CSRF token from the Django context or cookie
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
    window.confirmDeletion = confirmDeletion;

});

