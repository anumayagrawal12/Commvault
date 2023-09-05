const form = document.getElementById("upload_file_form");

const loadingSpinner = document.getElementById("loading-spinner"); // Replace with your spinner element's ID

// Show the loading spinner initially

// Add an event listener for the form submission
form.addEventListener("submit", function (event) {
  event.preventDefault(); // Prevent the default form submission

  // Get form data
  const formData = new FormData(form);

  // Access form fields by name
  const apiUrl = "/upload"; // Replace with your API endpoint URL

  // Create the fetch options for the POST request
  const fetchOptions = {
    method: "POST",
    body: formData, // Use the FormData object, which includes the file
  };

  // Send the POST request
  loadingSpinner.style.display = "block";
  fetch(apiUrl, fetchOptions)
    .then((response) => {
      return response.json(); // Parse the response JSON, if needed
    })
    .then((data) => {
      let status = data.status_code;
      if (status == 200) alert("File uploaded Successfully");
      else alert("Some Error Occured");
      for (let element of form.elements) {
        if (element.type !== "submit") {
          element.value = "";
        }
      }
      loadingSpinner.style.display = "none";
      // You can add code here to show a success message or redirect the user
    })
    .catch((error) => {
      console.error("API Error:", error);
      loadingSpinner.style.display = "none";
      // Handle errors, show error messages, etc.
    });

  // Add your JavaScript code to run when the form is submitted here
});
