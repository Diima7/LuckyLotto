
var overlay = document.getElementById('overlay');
var form = document.getElementById('hide');
var closeMenu = document.getElementById('close-menu');

document.getElementById('open-menu').addEventListener('click', menu_op);
document.getElementById('close-menu').addEventListener('click', menu_cl);
  
function menu_op(){
  overlay.classList.add('show-menu');
  form.classList.add('hide');
}

function menu_cl(){
  overlay.classList.remove('show-menu');
  form.classList.remove('hide');
}

