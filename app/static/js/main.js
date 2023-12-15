// To Make the image container of a post  card clickable
const user_container = document.querySelector('.author')
let z=user_container.getAttribute('data-author')
user_container.addEventListener("click", function () {
    console.log(z)
})
