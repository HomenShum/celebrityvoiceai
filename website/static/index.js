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

document.addEventListener("DOMContentLoaded", function () {
  const noteInput = document.querySelector("#note");
  const noteLengthText = document.querySelector("#note-length");

  noteInput.addEventListener("input", function () {
    const noteLength = this.value.length;
    noteLengthText.textContent = `${noteLength} / 500`;
  });

});

document.addEventListener("DOMContentLoaded", () => {
  const loadingSpinnerElement = document.getElementById("loading-spinner");
  const notesListElement = document.getElementById("loading-text");
  const messageElement = document.getElementById("note-form");
  const successElement = document.getElementById("success-text");
  const errorElement = document.getElementById("error-text");
  
  document.getElementById("note-form").addEventListener("submit", (event) => {
    event.preventDefault();

    const noteLength = document.querySelector("#note").value.length;

    if (noteLength > 500) {
      errorElement.classList.remove("d-none");
      successElement.classList.add("d-none");
      // timecountdown for 2 seconds, then add d-none to errorElement
      setTimeout(() => {
        errorElement.classList.add("d-none");
      }, 2000);
    } else {
      // timecountdown for 2 seconds, then add d-none to successElement
      errorElement.classList.add("d-none");
      successElement.classList.remove("d-none");
      setTimeout(() => {
        successElement.classList.add("d-none");
      }, 2000);

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
      }, 30000);

      // show timer countdown
      var countDownDate = new Date().getTime() + 30000;
      var x = setInterval(function () {
        var now = new Date().getTime();
        var distance = countDownDate - now;
        var seconds = Math.floor((distance % (1000 * 30)) / 1000);
        document.getElementById("timer").innerHTML = seconds + "s ";
        if (distance < 0) {
          clearInterval(x);
          document.getElementById("timer").innerHTML = "EXPIRED";
        }
      }, 1000);
    }
  });
});