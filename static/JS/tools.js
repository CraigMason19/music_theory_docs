function fetchToolResults() {
    const params = {};

    inputs.forEach(i => {
        params[i.dataset.key] = i.value;
    });

    const query = new URLSearchParams(params);

    fetch(`/documentation/tools/?${query.toString()}`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(res => res.json())
    .then(data => {
        displayResults(data)
    })
    .catch(err => console.error(err));
}

function displayResults(data) {
    document.getElementById('output').textContent = data.result;
    document.getElementById("list-result").textContent = data.my_list.join('\n');

    document.getElementById("mode-generator-results").textContent = data.mode_generator_results.join('\n');
}






const inputs = document.querySelectorAll(".ajax-input");

inputs.forEach(input => {
    input.addEventListener("change", fetchToolResults);
});

// Run on page load to show correct reults
window.addEventListener("DOMContentLoaded", fetchToolResults);





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