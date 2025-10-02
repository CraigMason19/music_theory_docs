const toolsForm = document.getElementById("tools-form");

// Tool 1
const toolOneNoteInput = document.getElementById("tool-one-note-input");
const toolOneKeyTypeInput = document.getElementById("tool-one-key-type-input");
const toolOneDominantInput = document.getElementById("tool-one-dominant-input");
const toolOneParallelInput = document.getElementById("tool-one-parallel-input");

// Tool 2
const toolTwoNoteInput = document.getElementById("tool-two-note-input");

// Tool 3
const toolThreeTuningInputOne = document.getElementById("tool-three-tuning-input-one");
const toolThreeTuningInputTwo = document.getElementById("tool-three-tuning-input-two");
const toolThreeTuningInputThree = document.getElementById("tool-three-tuning-input-three");
const toolThreeTuningInputFour = document.getElementById("tool-three-tuning-input-four");
const toolThreeTuningInputFive = document.getElementById("tool-three-tuning-input-five");
const toolThreeTuningInputSix = document.getElementById("tool-three-tuning-input-six");

const toolThreeFretInputOne = document.getElementById("tool-three-fret-input-one");
const toolThreeFretInputTwo = document.getElementById("tool-three-fret-input-two");
const toolThreeFretInputThree = document.getElementById("tool-three-fret-input-three");
const toolThreeFretInputFour = document.getElementById("tool-three-fret-input-four");
const toolThreeFretInputFive = document.getElementById("tool-three-fret-input-five");
const toolThreeFretInputSix = document.getElementById("tool-three-fret-input-six");

const inputs = [
    toolOneNoteInput,
    toolOneKeyTypeInput,
    toolOneDominantInput,
    toolOneParallelInput,

    toolTwoNoteInput,

    toolThreeTuningInputOne,
    toolThreeTuningInputTwo,
    toolThreeTuningInputThree,
    toolThreeTuningInputFour,
    toolThreeTuningInputFive,
    toolThreeTuningInputSix,

    toolThreeFretInputOne,
    toolThreeFretInputTwo,
    toolThreeFretInputThree,
    toolThreeFretInputFour,
    toolThreeFretInputFive,
    toolThreeFretInputSix,
]

// For all tool inputs, attach an event listener that resubmits the form if changes
inputs.forEach(i => {
    i.addEventListener("change", () => {
        toolsForm.submit()
    });
});


window.addEventListener("DOMContentLoaded", () => {
    const accordionHeaders = document.getElementsByClassName("accordion-header");

    for (let ah of accordionHeaders) {
        const panel = ah.nextElementSibling;

        if(panel != null) {
            // temporarily disable transition
            panel.classList.add("no-transition");

            // open all panels by default
            panel.style.maxHeight = panel.scrollHeight + "px";
            ah.classList.add("active");

            // allow browser to paint, then re-enable transition
            requestAnimationFrame(() => {
                panel.classList.remove("no-transition");
            });

            // click toggle
            ah.addEventListener("click", function() {
                this.classList.toggle("active");
                
                if (panel.style.maxHeight && panel.style.maxHeight !== "0px") {
                    panel.style.maxHeight = "0px"; // collapse
                } 
                else {
                    panel.style.maxHeight = panel.scrollHeight + "px"; // expand
                }
            });
        }
    }
});