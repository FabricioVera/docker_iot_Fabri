
const btnDelete= document.querySelectorAll('.btn-borrar');
if(btnDelete) {
  const btnArray = Array.from(btnDelete);
  btnArray.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      if(!confirm('¿Está seguro de querer borrar?')){
        e.preventDefault();
      }
    });
  })
}

let themestate;


function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  let expires = "expires="+d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
  let name = cname + "=";
  let ca = document.cookie.split(';');
  for(let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

// funcion cambiar de tema, recibiendo como parametro el nombre del tema
function changetheme(themestate){
  //si se manda una string como parametro se cambia el tema y se guarda el tema seleccionado en las cookies
  if (themestate){
    document.getElementById('estilos').setAttribute("href",`https://bootswatch.com/5/${themestate}/bootstrap.min.css`);
    setCookie("theme", themestate, 1);
  }
  else{
    document.getElementById('estilos').setAttribute("href",`https://bootswatch.com/5/darkly/bootstrap.min.css`);
  }
}
  
// escucha los botones de los temas
document.getElementById("cosmo").onclick = () => {changetheme("cosmo");}
document.getElementById("darkly").onclick = () => {changetheme("darkly");}

// cuando termina de cargar la pagina con los cookies obtiene los cookies
document.addEventListener("DOMContentLoaded", () => {changetheme(getCookie("theme"))});