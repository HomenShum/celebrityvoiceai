function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId })
    }).then((_res) => {
        window.location.href = "/";
    });
}


function deleteAllNotes() {
    fetch('/delete-all-notes', {
        method: 'POST'
    }).then(() => {
        window.location.href = "/";
    });
}

$(document).ready(function() {
    $("#toggleButton").click(function() {
        $("#navbarNav").toggleClass("showNav");
    });
});