// Create the query list.
const mediaQueryList = window.matchMedia("(max-width: 768px)");
const sidebar = document.querySelector("#main-sidenav");

sidebarCollapse = new bootstrap.Collapse(sidebar, {
  toggle: false
});

const handleMediaQueryChange = ()=>{
  sidebarCollapse.toggle();
};

// Exec when page is loading if media query matches
if (mediaQueryList.matches) {
  handleMediaQueryChange();
}

mediaQueryList.addEventListener('change', handleMediaQueryChange);
