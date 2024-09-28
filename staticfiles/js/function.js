$(document).ready(function() {
    // Check if the user has already submitted their email (from local storage)
    if (localStorage.getItem('emailSubmitted') === 'true') {
        $('#email-form').hide();
        $('#thankyou').show();
    }

    // AJAX form submission
    $('#email-form').on('submit', function(e) {
        e.preventDefault();  // Prevent the default form submission

        var email = $('#email').val();
        var csrfToken = $("input[name='csrfmiddlewaretoken']").val();

        $.ajax({
            type: 'POST',
            url: "save-email/",
            data: {
                'email': email,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                if (response.status === 'success') {
                    $('#email-form').hide();  // Hide the form
                    $('#thankyou').show();  // Show thank you message
                    localStorage.setItem('emailSubmitted', 'true');  // Set flag in local storage
                } else {
                    alert(response.message);  // Show error message
                }
            },
            error: function(xhr, status, error) {
                alert("Something went wrong. Please try again.");
            }
        });
    });
});

// Function to update the file name when a file is selected
function updateFileName() {
    const input = document.getElementById('profileImageInput');
    const fileNameDisplay = document.getElementById('fileName');

    if (input.files && input.files[0]) {
        // Display the selected file name
        fileNameDisplay.textContent = `Selected file: ${input.files[0].name}`;
    } else {
        fileNameDisplay.textContent = '';
    }
}
