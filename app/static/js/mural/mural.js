function collapseFunc(elementID) {
  var element = document.getElementById(elementID);
  console.log("Collapse gunc called")

  if ( element.classList.contains('d-none') ) {
    element.classList.remove('d-none');
    element.classList.add('d-block');
  }else{
    element.classList.remove('d-block');
    element.classList.add('d-none');
  }
}