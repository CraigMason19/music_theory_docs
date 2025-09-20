const toolsForm = document.getElementById("tools-form");

// Tool 1
const toolOneNoteInput = document.getElementById("tool-one-note-input");
const toolOneKeyTypeInput = document.getElementById("tool-one-key-type-input");
const toolOneDominantInput = document.getElementById("tool-one-dominant-input");
const toolOneParallelInput = document.getElementById("tool-one-parallel-input");

// Tool 2
const toolTwoNoteInput = document.getElementById("tool-two-note-input");

const inputs = [
    toolOneNoteInput,
    toolOneKeyTypeInput,
    toolOneDominantInput,
    toolOneParallelInput,
    toolTwoNoteInput,
]

inputs.forEach(i => {
    i.addEventListener("change", () => {
        toolsForm.submit()
    });
});