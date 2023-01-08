import { CSRF_ENDPOINT } from "../constants"
import { writable } from "svelte/store"
import { get } from "./apiHelper"

let csrfToken: string | null = null

export const obtainCsrf = async () => {
    if (csrfToken == null) {
        console.info('getting the csrf token')
        const response = await get(CSRF_ENDPOINT).then(s => s.json())
        csrfToken = response.csrfToken
    }
    return csrfToken ?? ''
}
