//Show/hide publication list
const hideOrShowPublicationList = () => {
    const showButton = document.getElementById('show-button');
    const hideButton = document.getElementById('hide-button');
    const publicationListContainer = document.getElementById('publication-list-container');
    if(publicationListContainer.classList.contains('hidden')){
        showButton.classList.add('hidden');
        hideButton.classList.remove('hidden');
        publicationListContainer.classList.remove('hidden');
    }else{
        showButton.classList.remove('hidden');
        hideButton.classList.add('hidden');
        publicationListContainer.classList.add('hidden');
    }
}

const addEvents = () => {
    const showButton = document.getElementById('show-button');
    const hideButton = document.getElementById('hide-button');
    showButton.addEventListener('click', hideOrShowPublicationList);
    hideButton.addEventListener('click', hideOrShowPublicationList);
}
addEvents();



