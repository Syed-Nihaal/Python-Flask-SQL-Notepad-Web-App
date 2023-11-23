// Function for deleting a note with the given noteId
function deleteNote(noteId) {
  // Sends a POST request to "/delete-note" with the note ID for deletion
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";  // Redirects to the home page after deleting the note
  });
}

// Function for updating a note with the given noteId and newData
function updateNote(noteId, newData) {
  // Sends a POST request to "/update-note" with the note ID and updated data
  fetch("/update-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId, newData: newData }),
  }).then((_res) => {
    window.location.href = "/";  // Redirects to the home page after updating the note
  });
}
