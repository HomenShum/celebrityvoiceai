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
    var noteLength = $(this).val().length; // get the length of the note
    $("#note-length").text(noteLength + " / 200"); // show the length
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const loadingSpinnerElement = document.getElementById("loading-spinner");
  const notesListElement = document.getElementById("loading-text");
  const messageElement = document.getElementById("note-form");

  document.getElementById("note-form").addEventListener("submit", (event) => {
    event.preventDefault();

    loadingSpinnerElement.classList.remove("d-none");
    notesListElement.classList.remove("d-none");
    messageElement.classList.add("d-none");

    const data = new FormData(event.target);

    fetch("/NelsonMandelaChat", {
      method: "POST",
      body: data,
    })
      .then((response) => response.json())
      .then((data) => {
        loadingSpinnerElement.classList.add("d-none");
        notesListElement.classList.add("d-none");
        messageElement.classList.remove("d-none");
        console.log(data);
      });
    // reload the page after 30 seconds
    setTimeout(() => {
      location.reload();
    }, 45000);

    // show timer countdown
    var countDownDate = new Date().getTime() + 45000;
    var x = setInterval(function () {
      var now = new Date().getTime();
      var distance = countDownDate - now;
      var seconds = Math.floor((distance % (1000 * 45)) / 1000);
      document.getElementById("timer").innerHTML = seconds + "s ";
      if (distance < 0) {
        clearInterval(x);
        document.getElementById("timer").innerHTML = "EXPIRED";
      }
    }, 1000);
  });
});
