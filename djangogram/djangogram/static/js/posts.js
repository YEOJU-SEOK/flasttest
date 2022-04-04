function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
 

const handleLikeClick = (buttonId) => {
    console.log(buttonId);

    const likeButton = document.getElementById(buttonId);
    const likeIcon = likeButton.querySelector("i");
    // ajax 방식의 경우 html에서 가진 csrf토큰이 없어서 403 에러 발생 가능성 높음
    const csrftoken = getCookie('csrftoken');

    // 서버로 좋아요 api 호출
    // buttonId에서 post.id추출
    const postID = buttonId.split("-").pop();

    const url = "/posts/" + postID + "/post_like/";
    
    fetch(url, {
        method: "POST",
        mode: "same-origin",
        headers: {'X-CSRFToken': csrftoken}
    })
    .then(response => response.json())
    .then(data => {
        if (data.result === "like") {
            // 좋아요 세팅
            // 결과를 받고 html(좋아요 하트) 모습을 변경
            likeIcon.classList.replace("fa-heart-o", "fa-heart"); 

        } else {
            // 좋아요 취소
            likeIcon.classList.replace("fa-heart", "fa-heart-o"); 
        }
    });

}
