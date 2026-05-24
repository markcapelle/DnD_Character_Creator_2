// NOTE TAB CLICK HANDLING
document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".note-tab").forEach(tab => {
        tab.addEventListener("click", () => {
            flushAutosave();
            
            const noteId = tab.dataset.noteId;

            // Highlight active tab
            document.querySelectorAll(".note-tab").forEach(t => t.classList.remove("active"));
            tab.classList.add("active");

            // Load note from server
            fetch(`/notebook/load/${noteId}`)
                .then(res => res.json())
                .then(data => {
                    if (data.error) {
                        alert(data.error);
                        return;
                    }

                    // Show editor
                    document.getElementById("no-note-selected").style.display = "none";
                    document.getElementById("note-editor").style.display = "block";

                    // Fill fields
                    document.getElementById("note-title-input").value = data.title;
                    document.getElementById("note-content-input").value = data.content;

                    // Store active note ID
                    document.getElementById("note-editor").dataset.activeNoteId = data.id;
                });
        });
    });


    // AUTOSAVE
    let autosaveTimer = null;

    function scheduleAutosave() {
        clearTimeout(autosaveTimer);
        autosaveTimer = setTimeout(saveActiveNote, 1500);
    }

    function flushAutosave() {
        clearTimeout(autosaveTimer);
        saveActiveNote(true); // synchronous save
    }

    function saveActiveNote(sync = false) {
        const editor = document.getElementById("note-editor");
        const noteId = editor.dataset.activeNoteId;
        if (!noteId) return;

        const title = document.getElementById("note-title-input").value;
        const content = document.getElementById("note-content-input").value;

        const payload = JSON.stringify({ title, content });

        if (sync) {
            const xhr = new XMLHttpRequest();
            xhr.open("POST", `/notebook/save/${noteId}`, false);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.send(payload);
            return;
        }

        fetch(`/notebook/save/${noteId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: payload
        });
    }


    // Attach autosave listeners
    document.getElementById("note-title-input").addEventListener("input", scheduleAutosave);
    document.getElementById("note-content-input").addEventListener("input", scheduleAutosave);

    document.getElementById("note-title-input").addEventListener("input", () => {
        const editor = document.getElementById("note-editor");
        const noteId = editor.dataset.activeNoteId;
        if (!noteId) return;

        const newTitle = document.getElementById("note-title-input").value;

        // Update the tab text immediately
        const tab = document.querySelector(`.note-tab[data-note-id="${noteId}"]`);
        if (tab) tab.textContent = newTitle;
    });




    // CREATE NEW NOTE
    document.getElementById("add-note-tab").addEventListener("click", () => {
    
        flushAutosave(); // Save current note before creating a new one
    
        const characterId = document.body.dataset.characterId;
    
        fetch(`/notebook/create/${characterId}`, {
            method: "POST"
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
    
            // Create new tab in the left column
            const newTab = document.createElement("div");
            newTab.classList.add("note-tab");
            newTab.dataset.noteId = data.id;
            newTab.textContent = data.title;
    
            // Insert above the Add New Note button
            const addTab = document.getElementById("add-note-tab");
            addTab.parentNode.insertBefore(newTab, addTab);
    
            // Remove active class from all tabs
            document.querySelectorAll(".note-tab").forEach(t => t.classList.remove("active"));
            newTab.classList.add("active");
    
            // Load the new note into the editor
            document.getElementById("no-note-selected").style.display = "none";
            document.getElementById("note-editor").style.display = "block";
    
            document.getElementById("note-title-input").value = data.title;
            document.getElementById("note-content-input").value = data.content;
    
            document.getElementById("note-editor").dataset.activeNoteId = data.id;
    
            // Attach click handler to the new tab
            newTab.addEventListener("click", () => {
                flushAutosave();
    
                const noteId = newTab.dataset.noteId;
    
                fetch(`/notebook/load/${noteId}`)
                    .then(res => res.json())
                    .then(note => {
                        document.querySelectorAll(".note-tab").forEach(t => t.classList.remove("active"));
                        newTab.classList.add("active");
    
                        document.getElementById("note-title-input").value = note.title;
                        document.getElementById("note-content-input").value = note.content;
                        document.getElementById("note-editor").dataset.activeNoteId = note.id;
                    });
            });
        });
    });



    // DELETE NOTE
    document.getElementById("delete-note-btn").addEventListener("click", () => {

        const editor = document.getElementById("note-editor");
        const noteId = editor.dataset.activeNoteId;
        if (!noteId) return;

        // Confirm deletion
        const confirmed = confirm("Are you sure you want to delete this note?");
        if (!confirmed) return;

        flushAutosave(); // Save any pending changes before deleting

        fetch(`/notebook/delete/${noteId}`, {
            method: "POST"
        })
        .then(res => res.json())
        .then(data => {
            if (!data.success) {
                alert("Error deleting note.");
                return;
            }

            // Remove tab from sidebar
            const tab = document.querySelector(`.note-tab[data-note-id="${noteId}"]`);
            if (tab) tab.remove();

            // Clear editor
            editor.style.display = "none";
            document.getElementById("no-note-selected").style.display = "block";

            document.getElementById("note-title-input").value = "";
            document.getElementById("note-content-input").value = "";

            delete editor.dataset.activeNoteId;
        });
    });
});
