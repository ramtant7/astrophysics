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

    let data = JSON.parse(event.data)
    let time = new Date().getTime()
    let xy = document.getElementById('imageXY')
    let xz = document.getElementById('imageXZ')
    let yz = document.getElementById('imageYZ')
    xy.src = data['xy'] + "?" + time
    xz.src = data['xz'] + "?" + time
    yz.src = data['yz'] + "?" + time
    console.log(xy)
    console.log(xy.src)
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

const inputFields = document.querySelectorAll('input');
const errorMessage = document.getElementById('error-message');

function checkParams() {
  // Проверка заполненности всех полей
  for (const inputField of inputFields) {
    if (inputField.value === '') {
      errorMessage.style.display = 'block';
      setTimeout(() => {
        errorMessage.style.display = 'none';
      }, 5000);
      return null;
    }
  }

  // Проверка значений
  const constraints = {

    eccentricity: { min: 0, max: 0.9999999999999999999999},
    'Semimajor axis': { min: 0.1, max: 999999999999999999999 },
    Mood: { min: 0, max: 360 },
    'Longitude of the ascending node': { min: 0, max: 360 },
    'Periapsis argument': { min: 0, max: 360 },
    'Average anomaly': { min: 0, max: 360 },
  };
  for (const inputField of inputFields) {
    const constraint = constraints[inputField.id];
    const value = Number(inputField.value);
    if (value < constraint.min || value > constraint.max) {
      errorMessage.style.display = 'block';
      setTimeout(() => {
        errorMessage.style.display = 'none';
      }, 5000);
      return null;
    }
  }

  return getTextValue()
}

function sendSimulationParam(param) {
    sendMessage(param)
}

function scrollDownContainer3() {
    var anchor = document.querySelector("[data-scroll-to='sranomalyscroll']");
    if(anchor) {
        anchor.scrollIntoView({"block":"start","behavior":"smooth"})
    }
}

function setLoadingImages() {
    let imageXY = document.getElementById("imageXY");
    let imageYZ = document.getElementById("imageYZ");
    let imageXZ = document.getElementById("imageXZ");

    console.log(imageXY)
    imageXY.src = "Loading.gif";
    imageYZ.src = "Loading.gif";
    imageXZ.src = "Loading.gif";
    console.log(imageXY)
}

var container3 = document.getElementById("container3");
if(container3) {
    container3.addEventListener("click", function () {
        let param = checkParams()
        if (param != null) {
            setLoadingImages()
            sendSimulationParam(param)
            scrollDownContainer3()
        }
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

// Для блока статистики, сколько дней прошло с начала проекта. В данном случае 8 декабря 2024 года
const currentDate = new Date();
const targetDate = new Date("December 9, 2024");
const timeDifference = Math.abs(targetDate.getTime() - currentDate.getTime());
const days = Math.ceil(timeDifference / (1000 * 60 * 60 * 24));
let daysText;

if (days % 10 === 1 && days % 100 !== 11) {
  daysText = "день";
} else if (days % 10 >= 2 && days % 10 <= 4 && (days % 100 < 10 || days % 100 >= 20)) {
  daysText = "дня";
} else {
  daysText = "дней";
}

document.getElementById("counter").innerHTML = "Проект существует " + days + " " + daysText;



// Создаёт красное поле ввода, если значение введено некорректно
const inputs = document.querySelectorAll('input');
const submitButton = document.querySelector('.div666');

const constraints = {
  eccentricity: {min: 0, max: 0.9999999999999999999999}, // ЗАМЕНИТЬ ОГРАНИЧЕНИЯ ПОД УСЛОВИЯ СИМУЛЯТОРА
  'Semimajor axis': {min: 0, max: 999999999999999999999}, // Проверка заполненности всех полей
  Mood: {min: 0, max: 360}, // ЗАМЕНИТЬ ОГРАНИЧЕНИЯ ПОД УСЛОВИЯ СИМУЛЯТОРА
  'Longitude of the ascending node': {min: 0, max: 360}, // ЗАМЕНИТЬ ОГРАНИЧЕНИЯ ПОД УСЛОВИЯ СИМУЛЯТОРА
  'Periapsis argument': {min: 0, max: 360}, // // ЗАМЕНИТЬ ОГРАНИЧЕНИЯ ПОД УСЛОВИЯ СИМУЛЯТОРА
  'Average anomaly': {min: 0, max: 360} // // ЗАМЕНИТЬ ОГРАНИЧЕНИЯ ПОД УСЛОВИЯ СИМУЛЯТОРА
};

inputs.forEach((input) => {
  input.addEventListener('input', (e) => {
    const value = e.target.value;
    const constraint = constraints[e.target.id];

    if (value < constraint.min || value > constraint.max) {
      e.target.classList.add('invalid');
      submitButton.disabled = true;
    } else {
      e.target.classList.remove('invalid');
      submitButton.disabled = false;
    }
  });
});

