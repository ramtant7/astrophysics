//  постоянное соединение
const socket = new WebSocket("ws://"+ location.host +"/ws");

socket.addEventListener('open', function (event) {
    console.log('Соединение установлено.');
});

socket.addEventListener('message', function (event) {
    console.log(event)
    let a = event.data
    console.log(a)
    let c = JSON.parse(a)
    console.log(c)
    let b = c['xy']
    console.log(b)

    let x = document.getElementById('image1')
    x.src = JSON.parse(event.data)['xy'] + "?" + new Date().getTime()
    console.log(x)
    console.log(x.src)
//    const messagesDiv = document.getElementById('messages');
//    const message = document.createElement('p');
//    message.textContent = `Сервер ответил: ${event.data}`;
//    messagesDiv.appendChild(message);
});

socket.addEventListener('close', function (event) {
    console.log('Соединение закрыто.', event);
});

socket.addEventListener('error', function (error) {
    console.error('Ошибка соединения:', error);
});

function sendMessage(message) {
    console.log(message)
    socket.send(JSON.stringify(message));
}


// вывод из полей ввода

function getTextValue() {
    let textInput1 = document.getElementById('eccentricity');                 // Получаем ссылку на элемент текстового поля
    E = textInput1.value;                                            // Извлекаем значение из текстового поля

    let textInput2 = document.getElementById('Semimajor axis');
    A = textInput2.value;

    let textInput3 = document.getElementById('Mood');
    I = textInput3.value;

    let textInput4 = document.getElementById('Longitude of the ascending node');
    Omega = textInput4.value;

    let textInput5 = document.getElementById('Periapsis argument');
    omega = textInput5.value;

    let textInput6 = document.getElementById('Average anomaly');
    M = textInput6.value;

    // Упаковываем переменные в объект
    const dataToSend = {
        'E': E,
        'A': A,
        'I': I,
        'Omega': Omega,
        'omega': omega,
        'M': M
    };
    return dataToSend

}



// кнопки

var container3 = document.getElementById("container3");
if(container3) {
    container3.addEventListener("click", function () {
        sendMessage( getTextValue() )
    });
}

var container = document.getElementById("container");
if(container) {
    container.addEventListener("click", function () {
            var anchor = document.querySelector("[data-scroll-to='container']");
            if(anchor) {
                anchor.scrollIntoView({"block":"start","behavior":"smooth"})
            }
    });
}


var container1 = document.getElementById("container1");
if(container1) {
    container1.addEventListener("click", function () {
            window.location.href = "PAGE_3.html";
    });
}

var container2 = document.getElementById("container2");
if(container2) {
    container2.addEventListener("click", function () {
            window.location.href = "PAGE_2.html";
    });
}