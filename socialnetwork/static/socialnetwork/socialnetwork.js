function getGlobal() {
    $.ajax({
        url:"/socialnetwork/get-global",
        type:"GET",
        dataType: "json",
        success: updateList,
        error: updateError
    });
}

function getFollower() {
    $.ajax({
        url:"/socialnetwork/get-follower",
        type:"GET",
        dataType: "json",
        success: updateList,
        error: updateError
    });
}

function updateError(xhr) {
    if (xhr.status === 0) {
        displayError("Cannot connect to server")
        return
    }

    if (!xhr.getResponseHeader('content-type') === 'application/json') {
        displayError("Received status=" + xhr.status)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}

function displayError(message) {
    $("#error").html(message);
}

function sanitize(s) {
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
}


function addComment(id) {
    let commentTextElement = $("#id_comment_input_text_"+id)
    let commentTextValue = commentTextElement.val()
    commentTextElement.val('')
    displayError('')
    $.ajax({
        url:'/socialnetwork/add-comment/'+id,
        type:"POST",
        data: "comment="+commentTextValue+"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType: 'json',
        success: (res) => {
            $("#comments_below"+id).append(
                     '<div id="id_comment_' + res.id + '">' +
                     '<div id="id_comment_div_' + res.id + '" style="text-align: left; margin-left: 40px">' +
                     '<i>Comment by </i>' +
                     '<a id="id_comment_profile_' + res.id + '"  href="/socialnetwork/view_profile/'+res.user_id+'">' + res.first_name + ' ' + res.last_name + '</a>--' +
                     '<span id="id_comment_text_' + res.id + '">' + sanitize(res.comments) + '</span>--' +
                     '<span id="id_comment_date_time_' + res.id + '" style="font-family: Arial">' + res.timestamp + '</span>' +
                     '</div><br>' +
                     '</div>'
                 )
        },
        error: updateError
    })
}

function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown";
}

function updateList(items) {
    for (var i = 0; i < items.length; i++) {
        let firstN = eval(JSON.stringify(items[i].firstname))
        let lastN = eval(JSON.stringify(items[i].lastname))
        let post = eval(JSON.stringify(items[i].post))
        let time = eval(JSON.stringify(items[i].timestamp))
        let id = eval(JSON.stringify(items[i].id))
        let userid = eval(JSON.stringify(items[i].userid))
        let thisid = "id_post_" + id

        if ( document.getElementById(thisid) == null ) {
            $("#posts-goes-here").append(
                '<div id="id_post_' + id + '">' +
                '<div id="id_post_div_' + id + '" style="text-align: left">' +
                '<i>Post by </i>' +
                '<a id="id_post_profile_' + id + '"  href="/socialnetwork/view_profile/'+userid+'">' + firstN + ' ' + lastN + '</a>--' +
                '<span id="id_post_text_' + id + '">' + post + '</span>--' +
                '<span id="id_post_date_time_' + id + '" style="font-family: Arial">' + time + '</span>' +
                '</div>' + '<br>' +
                '<ol id="comments_below'+id+'">' + '</ol>' +
                '<label for="id_comment_input_text_' + id + '">Comment: </label>' +
                '<input id="id_comment_input_text_' + id + '" style="width: 200px; height: 30px; font-size: large" name="comment">' +
                '<button id="id_comment_button_' + id + '" style="width: 70px; height: 40px; border-radius: 10px; background-color: lightskyblue" onclick="addComment(' + id + ')">Submit</button>' +
                '</div>'
            )
            for (var j = 0; j < items[i].comments.length; j++) {
                let getdata = items[i].comments[j]
                let comment = eval(JSON.stringify(getdata.comment))
                let firstn = eval(JSON.stringify(getdata.firstName))
                let lastn = eval(JSON.stringify(getdata.lastName))
                let commentime = eval(JSON.stringify(getdata.time))
                let comid = eval(JSON.stringify(getdata.id))
                let comuserid = eval(JSON.stringify(getdata.userid))
                // console.log(getdata)
                let checkid = "id_comment_"+comid
                if ( document.getElementById(checkid) == null) {
                    $("#comments_below"+id).append(
                     '<div id="id_comment_' + comid + '">' +
                     '<div id="id_comment_div_' + comid + '" style="text-align: left; margin-left: 40px">' +
                     '<i>Comment by </i>' +
                     '<a id="id_comment_profile_' + comuserid + '"  href="/socialnetwork/view_profile/'+userid+'">' + firstn + ' ' + lastn + '</a>--' +
                     '<span id="id_comment_text_' + comid + '">' + sanitize(comment) + '</span>--' +
                     '<span id="id_comment_date_time_' + comid + '" style="font-family: Arial">' + commentime + '</span>' +
                     '</div><br>' +
                     '</div>'
                 )
                }
            }


        }

    }

}
