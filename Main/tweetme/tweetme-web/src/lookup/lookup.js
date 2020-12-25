function lookup (method, endpoint, callback, data) {
    let jsonData

    if (data) {
        jsonData = JSON.stringify(data)
    }

    const xhr = new XMLHttpRequest()
    const url = `http://localhost:8000/api${endpoint}`
    const responseType = 'json'

    xhr.responseType = responseType
    xhr.open(method, url)

    xhr.onload = () => {
        callback(xhr.response, xhr.status)
    }

    xhr.onerror = () => {
        callback({'message': 'The request was an error'}, 400)
    }

    xhr.send(jsonData)
}

export function loadTweets (callback) {
    lookup('GET', '/tweets/', callback)
 } 