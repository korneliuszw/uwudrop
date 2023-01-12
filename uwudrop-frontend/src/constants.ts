import {
    PUBLIC_API_URL,
    PUBLIC_WEB_URL
} from '$env/static/public'
export const API_URL = PUBLIC_API_URL ?? "http://localhost:8050"

export const UPLOAD_START_ENDPOINT = "/uploader/begin"
export const UPLOAD_FILE_ENDPOINT = "/uploader/upload"
export const INVALIDATE_UPLOAD_ENDPOINT = "/uploader/invalidate"
export const CSRF_ENDPOINT = "/csrf"
export const DONWLOAD_ENDPOINT = "/download"
export const WEB_URL = PUBLIC_WEB_URL ?? "http://localhost:5173"

export const MAX_FILE_NAME_SIZE = 80