import { API_URL } from "../constants"
import { obtainCsrf } from "./csrf"
export enum ContentType {
    Json = "application/json",
    File = ""
}
interface PostHeaders {
    'X-CSRFToken': string;
    'Content-Type'?: string;
}
export const post = (endpoint: string, body: any, contentType: ContentType = ContentType.Json) => {
    return obtainCsrf().then(token => {
        let headers: PostHeaders = {
            'X-CSRFToken': token,
        }
        if (contentType !== ContentType.File) headers['Content-Type'] = contentType
        return fetch(API_URL + endpoint, {
            method: 'POST',
            body: (contentType === ContentType.Json) ? JSON.stringify(body) : body,
            headers,
            credentials: 'include' // TODO: Add switch for production
        })
    })
}


export const get = (endpoint: string, headers?: any) => {
    return fetch(API_URL + endpoint, {
        credentials: 'include',
        headers
    })
}