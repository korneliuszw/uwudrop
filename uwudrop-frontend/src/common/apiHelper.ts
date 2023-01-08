import { API_URL } from "src/constants"

export enum ContentType {
    Json = "application/json",
    Form = "multipart/form-data"
}

export const post = (endpoint: string, body: any, contentType: ContentType = ContentType.Json) => {
    return fetch(API_URL + endpoint, {
        method: 'POST',
        body: (contentType === ContentType.Json) ? JSON.stringify(body) : body,
        headers: {
            'Content-Type': contentType
        },
        credentials: 'include' // TODO: Add switch for production
    })
}
export const get = (endpoint: string) => {
    return fetch(API_URL + endpoint, {
        credentials: 'include'
    })
}