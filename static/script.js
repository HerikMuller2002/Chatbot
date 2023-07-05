//obtendo a url do servidor
const url = 'http://localhost:5000//chat'


//selecionando os elementos do DOM
const chatInput = document.querySelector(".chat__input")
const messageBtn = document.querySelector(".text__chat__button")
const  message = document.querySelector(".text__chat")
const exampleDiv = document.querySelector(".chat__demo-example")

document.querySelectorAll(".chat__demo-example").forEach((item) => {
    item.addEventListener("click", () => {
        message.value = item.textContent.trim()
    })
})


// adicionando o evento de click no botão de enviar
messageBtn.addEventListener("click", addMessage)
message.addEventListener("keyup", (e) => {
    if (e.keyCode === 13 ) {
        addMessage()
    }
})


// função para adicionar a mensagem do usuário e a resposta do servidor
async function typeText(text) {
    let textBot = document.querySelectorAll('.text');
    let currentTextBot = textBot[textBot.length - 1];
    let count = 0;
  
    const scrollIntoViewAsync = () => {
      return new Promise((resolve) => {
        setTimeout(() => {
          currentTextBot.scrollTop = currentTextBot.scrollHeight;
          resolve();
        }, 0);
      });
    };
  
    for (let i = 0; i < text.length; i++) {
      let letter = text[i];
      let link = '';
      let textArray = letter.text.split('');
  
      for (let j = 0; j < textArray.length; j++) {
        count += 1;
        let item = textArray[j];
  
        if (item === '¬') {
          currentTextBot.innerHTML += '<br>';
        } else {
          currentTextBot.innerHTML += item;
        }
  
        await scrollIntoViewAsync();
  
        if (textArray.length - 1 === j) {
          if ('link' in letter) {
            currentTextBot.innerHTML += `<br> <a href="${link}" target="_blank" class="pdf__link">Link para o pdf</a>.`;
          }
          if (i === text.length - 1) {
            setTimeout(() => {
              document.querySelector('.cursor').remove();
              chatInput.style.opacity = '1';
              chatInput.style.pointerEvents = 'all';
              chatInput.style.cursor = 'text';
              message.focus();
            }, 1200);
          } else {
            currentTextBot.innerHTML += '<br>' + '<br>';
          }
        }
      }
    }
  }
  
  function addMessage() {
    let userMessage = message.value;
  
    // verificando se o input está vazio
    if (message.value == '') {
      message.style.border = '1px solid red';
      message.style.boxShadow = '0 0 3px red';
      setTimeout(() => {
        message.style.border = '1px solid #ccc';
        message.style.boxShadow = 'none';
      }, 500);
      return;
    }
  
    // limpando o input
    message.value = '';
  
    // desabilitando o input
    chatInput.style.opacity = '.3';
    chatInput.style.pointerEvents = 'none';
    chatInput.style.cursor = 'not-allowed';
    document.querySelector('.text__chat').blur();
  
    // removendo a mensagem de demo
    const demoDiv = document.querySelector('.chat__demo');
    if (demoDiv) {
      demoDiv.remove();
    }
  
    // adicionando a mensagem do usuário
    let chatDiv = document.querySelector('.chat__messages');
    newDiv = `
      <div class="chat__message">
          <div class="icon__user icon">
              <i class='bx bxs-user'></i>
          </div>
          <div class="chat__message__text">
              <span class="text">
                  ${userMessage}
              </span>
          </div>
      </div>
      
    `;
    chatDiv.innerHTML += newDiv;
  
    const textUser = document.querySelectorAll('.chat__message__text');
    textUser[textUser.length - 1].scrollIntoView();
  
    if (textUser.length > 1) {
      textUser[textUser.length - 2].style.animation = 'none';
    }
    textUser[textUser.length - 1].style.animation = 'popUp .3s ease-in-out';
  
    // obtendo aresposta do servidor
    message.addEventListener('submit', (e) => {
      e.preventDefault();
    });
  
    sendMessage(userMessage)
      .then(async (res, e) => {
        newDiv = `
          <div class="chat__message bot__msg">
              <div class="icon__bot icon">
                  <i class='bx bxs-bot'></i>
              </div>
              <div class="chat__message__text__bot">
                  <span class="text"></span>
                  <span class="cursor">.</span>
              </div>
          </div>
        `;
        chatDiv.innerHTML += newDiv;
  
        await typeText(res);
      })
      .catch((error) => {
        textBot[textBot.length - 1].innerHTML = 'ERRO: Não foi possível conectar ao servidor.';
        divBot[divBot.length - 1].classList.add('chat__message__error');
        textBot[textBot.length - 1].scrollTop = textBot[textBot.length - 1].scrollHeight;
  
        setTimeout(() => {
          document.querySelector('.cursor').remove();
          chatInput.style.opacity = '1';
          chatInput.style.pointerEvents = 'all';
          chatInput.style.cursor = 'text';
          divBot[divBot.length - 1].style.animation = 'none';
          message.focus();
        }, 2200);
  
        throw error;
      });
  }
  


// fazendo a requisição para o servidor com fetch
async function sendMessage(message) {
    try {
        let req = await fetch(url, {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                'message': message,
                'clear_log': false
            }),
        })
        message.value = ""
        let res = await req.json()
        return res
    } catch (error) {
        return `ERRO ${error}. Não foi possível conectar ao servidor.`
    }
};


// limpando log ao dar reload
window.addEventListener("beforeunload", function() {
    const xhr = new XMLHttpRequest();
    const params = JSON.stringify({
        'message': '',
        'clear_log': true
    })

    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-type", "application/json; charset=utf-8");
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        console.log(xhr.responseText);
      }
    };
    xhr.send(params);
  });