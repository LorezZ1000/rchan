function exibirMensagemFlash() {
    var mensagem = "{{ get_flashed_messages()[0] }}" || "";
    if (mensagem) {
        alert(mensagem);
    }
}
window.onload = function() {
    exibirMensagemFlash();
    substituirSpoilers();
};
document.getElementById('postform').addEventListener('submit', function() {
    document.getElementById('postButton').disabled = true; 
});