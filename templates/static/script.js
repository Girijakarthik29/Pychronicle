const searchInput = document.getElementById("search");

searchInput.addEventListener("keyup", function () {
    let filter = searchInput.value.toLowerCase();
    let rows = document.querySelectorAll("table tbody tr");

    rows.forEach(function (row) {
        let variable = row.cells[1].textContent.toLowerCase();

        if (variable.includes(filter)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
});
let playInterval;

function playTrace(){

    let rows = document.querySelectorAll("tbody tr");

    currentIndex = -1;

    playInterval = setInterval(function(){

        if(currentIndex < rows.length-1){

            currentIndex++;

            rows.forEach(r => r.classList.remove("selected"));

            rows[currentIndex].classList.add("selected");

            let lineNo = rows[currentIndex].cells[0].innerText;

            highlightCodeLine(lineNo);

            document.getElementById("timeline").value = currentIndex;

        }
        else{

            clearInterval(playInterval);

        }

    },1000);

}

function stopTrace(){

    clearInterval(playInterval);

}