
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

let imagen = document.querySelectorAll("dropdown-item");
imagen.onclick=function(){
  if(document.getElementById('estilos').href==='https://bootswatch.com/5/cosmo/bootstrap.min.css'){
  document.getElementById('estilos').href='https://bootswatch.com/5/darkly/bootstrap.min.css';
  }else{
    document.getElementById('estilos').href='https://bootswatch.com/5/cosmo/bootstrap.min.css';
  }
}
