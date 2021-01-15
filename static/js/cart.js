const total = document.querySelector("#card_form #total");
const inputs = document.querySelectorAll("#card_form input");


totalUpdate();
document.querySelectorAll("#card_form img").forEach((img) => {
    img.addEventListener("click", (e) => {
        const action = e.currentTarget.dataset.action;
        const label = e.currentTarget.parentNode.parentNode;
        const input = label.querySelector("input");
        switch (action) {
            case "card_form_plus":
                input.value++;
                send();
                break;
            case "card_form_minus":
                if (Number(input.value) > 0) {
                    input.value--;
                    send();
                }
                if (Number(input.value) === 0) {
                    removeElement(label);
                }
                break;
            default:
                break;
        }
        totalUpdate();
    });
});

function send() {
    const form = document.querySelector("#card_form");
    const element = document.querySelector("#card_total_price")
    const body = new FormData(form);
    debug(body); // just for log, you can remove this line and function declaration
    fetch("cart_update/", {
        method: "POST",
        body,

    })
        .then(response => {
            console.log(response);
            return response.json()
        })  // convert to json
        .then(json => {
            element.textContent = json;
            console.log(json);

        })  //print data to console
        .catch(err => console.log('Request Failed', err)); // Catch errors
}

function removeElement(element) {
    element.parentNode.removeChild(element);
}

function totalUpdate() {
    let sum = 0;
    inputs.forEach((input) => {
        sum += input.value * input.dataset.price;
    });
    total.textContent = sum;

}

function debug(formData) {
    for (const pair of formData.entries()) {
        console.log(pair[0] + ", " + pair[1]);
    }
}
