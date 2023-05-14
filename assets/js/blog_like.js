const likeIcon = document.getElementById('like-icon');
const likeCount = document.getElementById('like-count');

likeIcon.onclick = () =>{
    const blogId = likeIcon.getAttribute('data-blog');
    const url = `/like/${parseInt(blogId)}/`;
    fetch(url, {
        method: 'GET',
        headers:{
            'content-type':'application/json'
        }
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if(data.liked){
            likeIcon.classList.remove('empty-heart');
        }
        else{
            likeIcon.classList.add('empty-heart');
        }
        likeCount.innerHTML = data.like_count;
    })
    .catch(error => {
        console.log(error);
    })
}