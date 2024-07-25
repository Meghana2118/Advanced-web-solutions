// scripts.js

document.addEventListener('DOMContentLoaded', function() {
    // Add event listener to form submission
    const createProductForm = document.querySelector('#create-product-form');
    if (createProductForm) {
        createProductForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default form submission
            const formData = new FormData(createProductForm); // Get form data

            // Optional: Add client-side validation logic here if needed

            // Send POST request to create product
            fetch('/create-product/', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    alert('Product created successfully!');
                    window.location.href = '/product-list/'; // Redirect to product list
                } else {
                    throw new Error('Failed to create product.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to create product. Please try again.');
            });
        });
    }
});
