export function loadTweets (callback) {
    const xhr = new XMLHttpRequest()
    const method = 'GET'
    const url = 'http://localhost:8000/api/tweets'
    const responseType = 'json'

    xhr.responseType = responseType
    xhr.open(method, url)

    xhr.onload = () => {
        callback(xhr.response, xhr.status)
    }

    xhr.onerror = () => {
        callback({'message': 'The request was an error'}, 400)
    }

    xhr.send()
 } 