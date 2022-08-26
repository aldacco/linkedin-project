// debes empezar desde la pagina 100
var array = []
for (var i = 0; i <= 30; i++) {
  setTimeout(() => {
    setTimeout(() => {
      var lista = document.querySelectorAll('.app-aware-link.scale-down')
      lista.forEach(e => {
        //console.log(e.href)
          array.push(e.href)
      })
    }, 2000)
    boton = document.querySelector('.ember-view > div > button')
    boton.click()
  }, i * 4000)
}