
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById("message-form");
  const dataEl = document.getElementById("user-data");
  const emisorId = dataEl.dataset.emisorId;
  const receptorId = dataEl.dataset.receptorId;
  const socket = io();
  socket.on("connect", () => {
    // Crear una room privada para el current user
    socket.emit("join", JSON.stringify({emisorId: emisorId}));
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
      })
    );
  }

  // Este evento Recibe todos los mensajes de mi receptor
  socket.on("mensaje_privado", (data)=>{
    console.log(data);
  });

  // Este evento significa que cree mi room
  socket.on("room_joined", (data)=>{
    console.log(data);
  });

  // Socket perdio conexion con el server
  socket.on("disconnect", () => {
    console.log("socket desconectado");
  });
});

