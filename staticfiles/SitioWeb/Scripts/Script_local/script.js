function close_messages (){
    document.getElementById('container-alert-messages').classList.toggle('close-menssages');
};

document.getElementById('button-close').onclick = function(){
    close_messages();
};
