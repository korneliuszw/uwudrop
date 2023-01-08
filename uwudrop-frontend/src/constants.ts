import {
    PUBLIC_API_URL
} from '$env/static/public'
export const API_URL = PUBLIC_API_URL ?? "http://localhost:8050"

export const UPLOAD_START_ENDPOINT = "/uploader/begin"
export const UPLOAD_FILE_ENDPOINT = "/uploader/upload"
export const INVALIDATE_UPLOAD_ENDPOINT = "/uploader/invalidate"