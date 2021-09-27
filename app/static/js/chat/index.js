
const scrollToNewMessage = function(){
  const referenceNewMessage = document.getElementById('there-is-a-new-message');
  referenceNewMessage.scrollIntoView({ behavior: 'smooth' });
}

document.addEventListener('DOMContentLoaded', () => {

  const messagesList = document.getElementById("messages-list-real-time");
  const form = document.getElementById("message-form");
  const dataEl = document.getElementById("user-data");
  const receiverPhoto = document.getElementById("receiver-photo").value;
  const senderPhoto = document.getElementById("sender-photo").value;
  const statusAmigoConexion = document.getElementById("status-amigo-conexion");
  const emisorId = dataEl.dataset.emisorId;
  const receptorId = dataEl.dataset.receptorId;
  const emisorName = dataEl.dataset.emisorName;
  const receptorName = dataEl.dataset.receptorName;
  const socket = io();

  // Variable gloabl para saber si mi amigo esta conectado
  let amigoConectado = false;

  socket.on("connect", () => {
    console.log("connected");
  });
  
  socket.on("amigo_conectado", (data)=>{
    statusAmigoConexion.innerHTML = `${data}`;
    statusAmigoConexion.setAttribute("class", "text-success");
    amigoConectado = true;
  });

  socket.on("amigo_desconectado", (data)=>{
    statusAmigoConexion.innerHTML = data;
    statusAmigoConexion.setAttribute("class", "text-danger");
    amigoConectado = false;
  });

  // Socket perdio conexion con el server
  socket.on("disconnect", () => {
    console.log("socket perdio conexion con el server");
  });

  form.onsubmit = (e) => {
    // Cuando usuario precione boton de enviar mensaje, prevenir
    // refresacar la pagina
    e.preventDefault();
    const message = form.message.value;
    // Mandar mensaje a la room privada de el amigo
    // con el que quieres chatear (receptor)
    socket.emit('message', JSON.stringify(
      {
        mensaje: message,
        receptorId: receptorId,
        emisorId: emisorId,
        receptorConectado: amigoConectado,
      })
    );

    var today = new Date();
    var date = today.getDate()+'-'+(today.getMonth()+1)+'-'+today.getFullYear();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    var dateTime = time+', '+date;

    form.message.value = '';
    let content = '';
    let newLi = document.createElement("li");
    newLi.setAttribute("class", "list-group-item border rounded shadow");
    let newArticle = document.createElement("article");
    newArticle.setAttribute("class", "d-flex flex-row-reverse gap-2 my-2 p-2");
    let newFigure =document.createElement("figure");
    newFigure.setAttribute("class", "position-relative");
    let newImg = document.createElement("img");
    newImg.setAttribute("src", senderPhoto);
    newImg.setAttribute("class", "m-1 amigo-lista-profile-icon rounded-circle");
    newFigure.appendChild(newImg);
    newArticle.appendChild(newFigure);

    let newSection = document.createElement("section");
    newSection.setAttribute("class", "d-flex flex-column");
    let newP1 = document.createElement("p");
    newP1.setAttribute("class", "text-end");
    content = document.createTextNode(emisorName);
    newP1.appendChild(content);
    let newDiv = document.createElement("div");
    newDiv.setAttribute("class", "d-flex flex-column gap-2 text-end");
    let newP2 = document.createElement("p");
    content = document.createTextNode(message);
    newP2.appendChild(content);
    let newP3 = document.createElement("p");
    content = document.createTextNode(dateTime);
    newP3.appendChild(content);
    newDiv.appendChild(newP2);
    newDiv.appendChild(newP3);
    newSection.appendChild(newP1);
    newSection.appendChild(newDiv);
    newArticle.appendChild(newSection);

    newLi.appendChild(newArticle);
    messagesList.appendChild(newLi);  

    scrollToNewMessage();

  }

  // Este evento Recibe todos los mensajes de mi receptor
  socket.on("mensaje_privado", (data)=>{

    var today = new Date();
    var date = today.getDate()+'-'+(today.getMonth()+1)+'-'+today.getFullYear();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    var dateTime = time+', '+date;

    console.log(data)
    let content = '';
    let newLi = document.createElement("li");
    newLi.setAttribute("class", "list-group-item border rounded shadow bg-light");
    let newArticle = document.createElement("article");
    newArticle.setAttribute("class", "d-flex gap-2 my-2 p-2");
    let newFigure =document.createElement("figure");
    newFigure.setAttribute("class", "position-relative");
    let newImg = document.createElement("img");
    newImg.setAttribute("src", receiverPhoto);
    newImg.setAttribute("class", "m-1 amigo-lista-profile-icon rounded-circle");
    newFigure.appendChild(newImg);
    newArticle.appendChild(newFigure);

    let newSection = document.createElement("section");
    newSection.setAttribute("class", "d-flex flex-column");
    let newP1 = document.createElement("p");
    newP1.setAttribute("class", "text-end");
    content = document.createTextNode(receptorName);
    newP1.appendChild(content);
    let newDiv = document.createElement("div");
    newDiv.setAttribute("class", "d-flex flex-column gap-2");
    let newP2 = document.createElement("p");
    content = document.createTextNode(data);
    newP2.appendChild(content);
    let newP3 = document.createElement("p");
    content = document.createTextNode(dateTime);
    newP3.appendChild(content);
    newDiv.appendChild(newP2);
    newDiv.appendChild(newP3);
    newSection.appendChild(newP1);
    newSection.appendChild(newDiv);
    newArticle.appendChild(newSection);

    newLi.appendChild(newArticle);
    messagesList.appendChild(newLi);

    scrollToNewMessage();
  
  });

});

