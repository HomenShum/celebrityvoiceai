function deleteNote(noteId) {
  $.ajax({
    url: "/delete-note",
    type: "POST",
    data: JSON.stringify({ noteId: noteId }),
    contentType: "application/json",
    success: function () {
      location.reload();
    },
    error: function (xhr) {
      alert(xhr.responseText);
    },
  });
}

function deleteAllNotes() {
  $.ajax({
    url: "/delete-all-notes",
    type: "POST",
    success: function () {
      location.reload(); // reload the current page
    },
    error: function (xhr) {
      alert(xhr.responseText);
    },
  });
}

$(document).ready(function () {
  // Show the character count for the note input field
  $("#note").on("input", function () {
    var noteLength = $(this).val().length;
    $("#note-length").text(noteLength + " / 200");
  });
});
